#!/usr/bin/env python3
"""
Mentor Governance Evaluation -- deterministic, read-only governance
classification for a child repository's declared rules and exceptions
against Mentor's own standing precedence order.

This script implements, AS CODE, the one genuinely deterministic part
of docs/Governance Precedence Model.md: given a governance tier (or
pair of tiers) and an already-determined relationship between two
requirements, what conflict type (Section 10) and expected handling
(Section 11) follows. It does not define a second precedence hierarchy
and does not restate that document's prose -- it is the executable
form of its Sections 3-11, and nothing more.

What this script deliberately does NOT do (see docs/Governance
Evaluation.md for the full responsibility boundary and why):

  - It does not determine whether a specific child rule's declared
    `scope` actually covers a specific diff/file under review. Free-text
    scope-to-code matching requires reading the actual code, which this
    script never receives -- docs/Child Rules and Exceptions.md Section 6
    explicitly defers "exact scope-matching semantics" as future work,
    and this script does not invent that matching. That determination
    ("applicability"), and the relationship a specific child rule bears
    to a specific Mentor requirement ("does it narrow the requirement,
    or does it assert the requirement doesn't apply?"), are supplied as
    INPUT by the caller -- a Skill, using its own judgment against the
    actual material under review -- via `--assertions`. This mirrors
    exactly how skills/code-review/SKILL.md's own Child Governance rules
    already determine applicability today; this script only takes over
    the deterministic classification step that follows that judgment.

  - It does not determine finding severity. Severity is, and remains,
    entirely the calling Skill's responsibility, governed solely by
    context/standards/Severity Taxonomy.md. No key in this script's
    output is named "severity", and none should ever be added.

  - It does not parse .mentor/project.yaml, .mentor/rules/, or
    .mentor/exceptions.yaml itself. It consumes the JSON already
    produced by scripts/discover_project_context.py,
    scripts/validate_child_rule.py, and scripts/validate_exceptions_yaml.py
    -- reusing them directly (as Python function calls, in --repo-root
    convenience mode) rather than re-implementing any parsing.

  - It never writes to, modifies, or creates anything in a child
    repository, in .mentor/, or in Mentor's own governance. It performs
    no file writes at all (aside from stdout).

Two invocation modes:

  1. Convenience mode (recommended -- what skills/code-review/SKILL.md
     uses):
       python3 scripts/evaluate_governance.py <repo-root> --assertions <assertions.json> [--json]
     Internally calls discover_project_context.discover(),
     validate_child_rule.validate_rules_dir(), and
     validate_exceptions_yaml.validate_file() directly (Python function
     calls -- no re-implementation, no shelling out to another script)
     to build the structural rule/exception catalog, then applies
     `--assertions` on top of it.

  2. Composed mode (for testing, or when discovery/validation output is
     already on hand as JSON):
       python3 scripts/evaluate_governance.py --context context.json \\
           --rules rules.json --exceptions exceptions.json \\
           --assertions assertions.json [--json]
     `context.json` is scripts/discover_project_context.py's own output
     (or any subset with the same shape: mentorConfigured, projectProfile,
     childRules, exceptions). `rules.json` is the output of
     `validate_child_rule.py --dir <dir> --json`. `exceptions.json` is
     the output of `validate_exceptions_yaml.py <path> --json`. Either
     or both of `--rules`/`--exceptions` may be omitted when nothing was
     declared for that artifact.

`--assertions` file shape (always required -- see docs/Governance
Evaluation.md for the full field reference and worked examples):

    {
      "requirements": [
        {
          "ruleId": "<a discovered child rule's id>",
          "mentorRequirementTier": "security_safety" | "mentor_mandatory"
              | "mentor_configurable_boundary" | "mentor_advisory" | "informational",
          "mentorRequirementDescription": "<free text, carried through for reporting only>",
          "applicability": "applies" | "not_applicable" | "unknown",
          "relationship": "unrelated" | "narrows" | "replaces" | "disagrees"
              | "asserts_exempt" | "unknown"
        }, ...
      ],
      "exceptions": [
        {
          "exceptionId": "<a discovered exception's id>",
          "targetRuleTier": "<same vocabulary as mentorRequirementTier, or a
              child tier ('child_mandatory' etc.) if the exception targets a
              child rule rather than a Mentor requirement>",
          "targetRuleDescription": "<free text, for reporting only>",
          "applicability": "applies" | "not_applicable" | "unknown"
        }, ...
      ]
    }

An entry in `requirements`/`exceptions` whose `ruleId`/`exceptionId`
does not match anything in the discovered catalog is reported as its
own warning and otherwise ignored -- this script never evaluates a
rule/exception that discovery/validation didn't actually find.

Exit codes:
    0 - evaluation completed (true even when every requirement turns
        out to be a Prohibited Override, or context is missing/invalid
        -- those are reported in the result, not failures of this
        script)
    2 - usage error (bad arguments, unreadable input file, malformed
        JSON in any input, malformed --assertions structure)
"""
import sys
import json
import argparse
import re
from pathlib import Path as _Path

sys.path.insert(0, str(_Path(__file__).resolve().parent))
import discover_project_context  # noqa: E402
from validate_child_rule import validate_rules_dir  # noqa: E402
from validate_exceptions_yaml import validate_file as validate_exceptions_file  # noqa: E402

# ---------------------------------------------------------------------
# The standing precedence order, restated as code exactly once, from
# docs/Governance Precedence Model.md Section 4. Ranks 1-2 are the
# absolute floor (Sections 3-5): nothing below can ever legitimately
# supersede them, regardless of a child rule's own classification
# label or relative tier. "mentor_configurable_boundary" shares rank 2
# because Section 7 states the boundary itself -- as opposed to the
# specific value a child selects within it -- is exactly as
# non-negotiable as a Mandatory rule.
# ---------------------------------------------------------------------
TIER_RANKS = {
    "security_safety": 1,
    "mentor_mandatory": 2,
    "mentor_configurable_boundary": 2,
    "child_mandatory": 3,
    "child_configurable": 4,
    "child_advisory": 5,
    "mentor_advisory": 6,
    "informational": 7,
}
FLOOR_RANK = 2

CLASSIFICATION_TO_CHILD_TIER = {
    "mandatory": "child_mandatory",
    "configurable": "child_configurable",
    "advisory": "child_advisory",
    "informational": "child_informational",
}

VALID_APPLICABILITY = {"applies", "not_applicable", "unknown"}
VALID_RELATIONSHIP = {"unrelated", "narrows", "replaces", "disagrees", "asserts_exempt", "unknown"}
INACTIVE_EXCEPTION_STATUSES = {"rejected", "expired"}


def classify_relationship(mentor_tier, child_tier, relationship):
    """The one pure, deterministic function this whole script exists to
    provide. Given the Mentor-side requirement's tier, the child-side
    requirement's tier, and an already-determined relationship between
    them, returns (conflictType, handling) per docs/Governance
    Precedence Model.md Sections 10-11.

    Both tier arguments accept any key from TIER_RANKS -- this
    function is intentionally tier-agnostic about *which* side is
    "Mentor" and which is "child" (Section 10's Conflict category
    applies just as well between two child rules, e.g. two Configurable
    rules from different declared conventions disagreeing with each
    other -- Test 14 in the deterministic suite exercises exactly
    this). The one place tier *identity* (not just rank) matters is the
    single documented Override case (Section 8): Child Advisory
    replacing Mentor Advisory specifically -- no broader override rule
    is invented for any other tier pairing, per the No Invention
    constraint on this phase.
    """
    if relationship == "unknown":
        return "unknown", "insufficient_evidence"

    rank_mentor = TIER_RANKS.get(mentor_tier)
    rank_child = TIER_RANKS.get(child_tier)
    if rank_mentor is None or rank_child is None:
        return "unknown", "insufficient_evidence"

    if relationship == "unrelated":
        return "compatible", "apply_both"

    if relationship == "narrows":
        # Additive governance is available at every tier a child rule
        # can occupy (docs/Governance Precedence Model.md Section 6) --
        # narrowing how a requirement is satisfied never contests that
        # it applies, regardless of either side's tier.
        return "additive", "apply_both"

    # relationship in ("replaces", "disagrees", "asserts_exempt"): the
    # child side is attempting to supersede, contest, or exempt itself
    # from the Mentor-side requirement.
    if rank_mentor <= FLOOR_RANK:
        # Absolute floor (Sections 3-5): a Mentor Mandatory rule, a
        # security/safety requirement, or a Mentor Configurable rule's
        # own outer boundary. Nothing below can legitimately weaken it,
        # no matter the child rule's own classification label or tier.
        return "prohibited_override", "preserve_mentor_and_flag"

    if mentor_tier == "mentor_advisory" and child_tier == "child_advisory" and relationship == "replaces":
        # The one specifically documented Override case (Section 8).
        return "override", "use_child"

    if rank_child < rank_mentor:
        # The child side's own tier structurally outranks the Mentor
        # side's tier in the standing order, but this isn't the one
        # documented Override shape above -- docs/Governance Precedence
        # Model.md does not specify a broader override rule for any
        # other tier pairing, so this is conservatively surfaced as a
        # Conflict (favoring the child side) rather than inventing a
        # new Override category.
        return "conflict", "surface_conflict_child_favored"

    if rank_child == rank_mentor:
        # Two same-tier requirements from different sources genuinely
        # disagree (e.g. two Child Advisory/Configurable rules, or two
        # Mentor-tier requirements) -- Section 10's "Conflict (true)"
        # category, with no tie-break specified in the source document,
        # so none is invented here.
        return "conflict", "surface_conflict_tied"

    # The child side's tier is lower-precedence than the Mentor side's
    # tier, and the Mentor side isn't at the absolute floor -- the
    # child side cannot legitimately supersede it, but this also isn't
    # a Prohibited Override (that category is reserved for the floor,
    # Sections 3-5). Surfaced as Conflict, favoring the Mentor side.
    return "conflict", "surface_conflict_mentor_favored"


def evaluate_exception_relationship(target_tier, applicability, status):
    """The exception-specific counterpart to classify_relationship().
    An exception is never a governance tier of its own (docs/Governance
    Precedence Model.md Section 9) -- it is evaluated relative to
    whatever tier the rule it names sits at, using the same floor
    invariant, but never producing "additive"/"compatible"/"override"
    outcomes an exception structurally cannot be (an exception is
    always, by definition, an attempted deviation -- assertion =
    asserts_exempt is implicit)."""
    if status in INACTIVE_EXCEPTION_STATUSES:
        return "inactive", "none"
    if applicability == "unknown":
        return "unknown", "insufficient_evidence"
    if applicability == "not_applicable":
        return "not_applicable", "none"

    rank = TIER_RANKS.get(target_tier)
    if rank is None:
        return "unknown", "insufficient_evidence"
    if rank <= FLOOR_RANK:
        # Section 9: an exception is not exempt from the Prohibited
        # Override category merely because its own status is
        # "approved" -- the rule/requirement it names, not the
        # exception's own recorded status, determines this.
        return "prohibited_override", "preserve_mentor_and_flag"

    # Below the floor: a legitimate, bounded, informational deviation.
    # This phase never suppresses/downgrades a finding because of this
    # outcome (docs/Governance Precedence Model.md Section 13) -- that
    # remains the calling Skill's decision to make, or not make.
    return "exception_applicable", "informational_only_no_suppression"


# ---------------------------------------------------------------------
# Structural catalog builders -- consume already-parsed JSON, never
# parse .mentor/ content themselves.
# ---------------------------------------------------------------------

def build_rules_catalog(rules_json, warnings):
    """`rules_json` is the shape emitted by
    `validate_child_rule.py --dir <dir> --json` (post the frontmatter
    fix applied this phase): {"valid", "files": {name: {valid,
    frontmatter, errors, warnings}}, "directoryErrors"}. Returns a list
    of catalog entries, each carrying validity, tier, and status."""
    catalog = []
    if not rules_json:
        return catalog

    for name, entry in sorted(rules_json.get("files", {}).items()):
        fm = entry.get("frontmatter") or {}
        valid = bool(entry.get("valid"))
        classification = fm.get("classification")
        tier = CLASSIFICATION_TO_CHILD_TIER.get(classification)
        cat_entry = {
            "id": fm.get("id"),
            "file": name,
            "valid": valid,
            "classification": classification,
            "tier": tier,
            "scope": fm.get("scope"),
            "status": fm.get("status", "active") if valid else None,
            "errors": entry.get("errors", []),
        }
        catalog.append(cat_entry)
        if not valid:
            warnings.append(
                "child rule '{}' failed validation and is not treated as active governance: {}".format(
                    name, "; ".join(e.get("code", "?") for e in entry.get("errors", []))
                )
            )
    for derr in rules_json.get("directoryErrors", []):
        warnings.append("child rules directory error: {}".format(derr.get("message", derr)))
    return catalog


_ENTRY_INDEX_RE = re.compile(r"^\[(\d+)\]")


def build_exceptions_catalog(exceptions_json, warnings):
    """`exceptions_json` is the shape emitted by
    `validate_exceptions_yaml.py <path> --json` (post the entries fix
    applied this phase): {"valid", "entries", "errors", "warnings"}.
    Per-entry errors (path starting "[N]") are attributed to entry N;
    an entry with any error against it is excluded from active
    governance but still listed, with valid=False."""
    catalog = []
    if not exceptions_json:
        return catalog

    entries = exceptions_json.get("entries")
    if entries is None:
        if exceptions_json.get("errors"):
            warnings.append(
                "exceptions.yaml failed validation and is not treated as active governance: {}".format(
                    "; ".join(e.get("code", "?") for e in exceptions_json["errors"])
                )
            )
        return catalog

    errors_by_index = {}
    for e in exceptions_json.get("errors", []):
        m = _ENTRY_INDEX_RE.match(e.get("path", ""))
        if m:
            errors_by_index.setdefault(int(m.group(1)), []).append(e)

    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            continue
        entry_errors = errors_by_index.get(i, [])
        valid = len(entry_errors) == 0
        cat_entry = {
            "id": entry.get("id"),
            "rule": entry.get("rule"),
            "scope": entry.get("scope"),
            "status": entry.get("status") if valid else None,
            "expiresAt": entry.get("expiresAt"),
            "valid": valid,
            "errors": [e for e in entry_errors],
        }
        catalog.append(cat_entry)
        if not valid:
            warnings.append(
                "exception entry '{}' (index {}) failed validation and is not treated as active governance: {}".format(
                    entry.get("id", "?"), i, "; ".join(e.get("code", "?") for e in entry_errors)
                )
            )
    return catalog


# ---------------------------------------------------------------------
# Top-level evaluation
# ---------------------------------------------------------------------

def evaluate(context, rules_json, exceptions_json, assertions):
    warnings = []
    context = context or {}

    mentor_configured = bool(context.get("mentorConfigured"))
    project_profile = context.get("projectProfile") or {}
    child_context_valid = None
    if project_profile.get("declared"):
        child_context_valid = bool(project_profile.get("valid"))
        if child_context_valid is False:
            warnings.append("project.yaml failed validation -- declared fields are unverified, not treated as authoritative")

    if not mentor_configured:
        warnings.append("no .mentor/ configuration discovered -- no child rules or exceptions exist to evaluate")

    rules_catalog = build_rules_catalog(rules_json, warnings)
    exceptions_catalog = build_exceptions_catalog(exceptions_json, warnings)

    rules_by_id = {r["id"]: r for r in rules_catalog if r.get("id")}
    exceptions_by_id = {e["id"]: e for e in exceptions_catalog if e.get("id")}

    applicable_requirements = []
    assertions = assertions or {}
    for req in assertions.get("requirements", []):
        rule_id = req.get("ruleId")
        rule = rules_by_id.get(rule_id)
        if rule is None:
            warnings.append("assertion references ruleId '{}', which was not found in the discovered/validated rule catalog -- ignored".format(rule_id))
            continue
        if not rule["valid"]:
            warnings.append("assertion references ruleId '{}', which failed rule validation -- ignored, not evaluated as active governance".format(rule_id))
            continue

        applicability = req.get("applicability")
        relationship = req.get("relationship")
        if applicability not in VALID_APPLICABILITY or relationship not in VALID_RELATIONSHIP:
            warnings.append("assertion for ruleId '{}' has an invalid applicability/relationship value -- ignored".format(rule_id))
            continue

        entry = {
            "ruleId": rule_id,
            "childTier": rule["tier"],
            "scope": rule["scope"],
            "status": rule["status"],
            "mentorRequirementTier": req.get("mentorRequirementTier"),
            "mentorRequirementDescription": req.get("mentorRequirementDescription"),
            "applicability": applicability,
            "relationship": relationship,
        }

        if rule["status"] == "deprecated":
            entry["classification"] = "not_applicable"
            entry["handling"] = "none"
        elif applicability == "not_applicable":
            entry["classification"] = "not_applicable"
            entry["handling"] = "none"
        elif applicability == "unknown":
            entry["classification"] = "unknown"
            entry["handling"] = "insufficient_evidence"
        else:
            classification, handling = classify_relationship(
                req.get("mentorRequirementTier"), rule["tier"], relationship
            )
            entry["classification"] = classification
            entry["handling"] = handling

        applicable_requirements.append(entry)

    exception_evaluations = []
    for exc_assert in assertions.get("exceptions", []):
        exc_id = exc_assert.get("exceptionId")
        exc = exceptions_by_id.get(exc_id)
        if exc is None:
            warnings.append("assertion references exceptionId '{}', which was not found in the discovered/validated exception catalog -- ignored".format(exc_id))
            continue
        if not exc["valid"]:
            warnings.append("assertion references exceptionId '{}', which failed exception validation -- ignored, not evaluated as active governance".format(exc_id))
            continue

        applicability = exc_assert.get("applicability")
        if applicability not in VALID_APPLICABILITY:
            warnings.append("assertion for exceptionId '{}' has an invalid applicability value -- ignored".format(exc_id))
            continue

        classification, handling = evaluate_exception_relationship(
            exc_assert.get("targetRuleTier"), applicability, exc["status"]
        )
        exception_evaluations.append({
            "exceptionId": exc_id,
            "rule": exc["rule"],
            "scope": exc["scope"],
            "status": exc["status"],
            "expiresAt": exc["expiresAt"],
            "targetRuleTier": exc_assert.get("targetRuleTier"),
            "targetRuleDescription": exc_assert.get("targetRuleDescription"),
            "applicability": applicability,
            "classification": classification,
            "handling": handling,
        })

    conflicts = [r for r in applicable_requirements if r["classification"] == "conflict"]
    prohibited_overrides = (
        [r for r in applicable_requirements if r["classification"] == "prohibited_override"]
        + [e for e in exception_evaluations if e["classification"] == "prohibited_override"]
    )
    advisory_overrides = [r for r in applicable_requirements if r["classification"] == "override"]
    insufficient_evidence = (
        [r for r in applicable_requirements if r["classification"] == "unknown"]
        + [e for e in exception_evaluations if e["classification"] == "unknown"]
    )

    return {
        "mentorConfigured": mentor_configured,
        "childContextValid": child_context_valid,
        "childRules": rules_catalog,
        "exceptions": exceptions_catalog,
        "applicableRequirements": applicable_requirements,
        "exceptionEvaluations": exception_evaluations,
        "conflicts": conflicts,
        "prohibitedOverrides": prohibited_overrides,
        "advisoryOverrides": advisory_overrides,
        "insufficientEvidence": insufficient_evidence,
        "warnings": warnings,
    }


def evaluate_from_repo_root(root, assertions):
    context = discover_project_context.discover(root)

    rules_json = None
    if context.get("childRules", {}).get("declared"):
        mentor_dir = _Path(context["projectRoot"]) / ".mentor"
        rules_dir = mentor_dir / "rules"
        per_file, dir_findings = validate_rules_dir(rules_dir)
        rules_json = {
            "valid": not any(f.level == "error" for _fn, (_fm, fs) in per_file.items() for f in fs) and not dir_findings,
            "files": {
                fname: {
                    "valid": len([f for f in fs if f.level == "error"]) == 0,
                    "frontmatter": fm if isinstance(fm, dict) else None,
                    "errors": [f.to_dict() for f in fs if f.level == "error"],
                    "warnings": [f.to_dict() for f in fs if f.level == "warning"],
                }
                for fname, (fm, fs) in per_file.items()
            },
            "directoryErrors": [f.to_dict() for f in dir_findings],
        }

    exceptions_json = None
    if context.get("exceptions", {}).get("declared") and context["exceptions"].get("path"):
        exc_path = _Path(context["projectRoot"]) / context["exceptions"]["path"]
        doc, findings = validate_exceptions_file(str(exc_path))
        exceptions_json = {
            "valid": not any(f.level == "error" for f in findings),
            "entries": doc if isinstance(doc, list) else None,
            "errors": [f.to_dict() for f in findings if f.level == "error"],
            "warnings": [f.to_dict() for f in findings if f.level == "warning"],
        }

    return evaluate(context, rules_json, exceptions_json, assertions)


def _load_json_file(path):
    try:
        return json.loads(_Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print("error: could not read/parse {}: {}".format(path, e), file=sys.stderr)
        sys.exit(2)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("repo_root", nargs="?", help="child repository root (convenience mode)")
    parser.add_argument("--context", help="path to discover_project_context.py output JSON (composed mode)")
    parser.add_argument("--rules", help="path to validate_child_rule.py --dir --json output (composed mode)")
    parser.add_argument("--exceptions", help="path to validate_exceptions_yaml.py --json output (composed mode)")
    parser.add_argument("--assertions", required=True, help="path to the caller-supplied assertions JSON (see module docstring)")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON (default: also JSON, this flag is accepted for CLI-convention parity with the other validators)")
    args = parser.parse_args()

    assertions = _load_json_file(args.assertions)
    if not isinstance(assertions, dict):
        print("error: --assertions file must contain a JSON object", file=sys.stderr)
        sys.exit(2)

    if args.repo_root:
        if args.context or args.rules or args.exceptions:
            print("error: pass either a repo_root (convenience mode) or --context/--rules/--exceptions (composed mode), not both", file=sys.stderr)
            sys.exit(2)
        root_path = _Path(args.repo_root)
        if not root_path.is_dir():
            print("error: {} is not a directory".format(args.repo_root), file=sys.stderr)
            sys.exit(2)
        result = evaluate_from_repo_root(root_path, assertions)
    else:
        if not args.context:
            print("error: either repo_root or --context is required", file=sys.stderr)
            sys.exit(2)
        context = _load_json_file(args.context)
        rules_json = _load_json_file(args.rules) if args.rules else None
        exceptions_json = _load_json_file(args.exceptions) if args.exceptions else None
        result = evaluate(context, rules_json, exceptions_json, assertions)

    print(json.dumps(result, indent=2, sort_keys=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
