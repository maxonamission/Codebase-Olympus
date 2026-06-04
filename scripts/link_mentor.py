#!/usr/bin/env python3
"""CLI: link a mentor to a learner (F2-01).

Usage:
    uv run python scripts/link_mentor.py <mentor_email> <learner_email>
    uv run python scripts/link_mentor.py --db path/to.db <mentor_email> <learner_email>

The script promotes the mentor account to the MENTOR role if it is still a
learner, then records a mentor->learner assignment. Both accounts must
already exist. Re-running with the same pair is a no-op.
"""

import argparse
import sys
from pathlib import Path

from gymnasium_classica.api.database import (
    DEFAULT_DB_PATH,
    create_mentor_assignment,
    get_user_by_email,
    init_db,
    update_user,
)
from gymnasium_classica.models.user import Role


def main() -> None:
    parser = argparse.ArgumentParser(description="Link a mentor to a learner.")
    parser.add_argument("mentor_email", help="Email of the mentor account")
    parser.add_argument("learner_email", help="Email of the learner account")
    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB_PATH,
        help=f"Path to the SQLite database (default: {DEFAULT_DB_PATH})",
    )
    args = parser.parse_args()

    conn = init_db(args.db)

    mentor = get_user_by_email(conn, args.mentor_email)
    if mentor is None:
        print(f"ERROR: no user with email {args.mentor_email!r}", file=sys.stderr)
        sys.exit(1)

    learner = get_user_by_email(conn, args.learner_email)
    if learner is None:
        print(f"ERROR: no user with email {args.learner_email!r}", file=sys.stderr)
        sys.exit(1)

    if mentor.id == learner.id:
        print("ERROR: a user cannot be their own mentor", file=sys.stderr)
        sys.exit(1)

    if mentor.role != Role.MENTOR:
        mentor.role = Role.MENTOR
        update_user(conn, mentor)
        print(f"Promoted {mentor.email} to MENTOR role.")

    create_mentor_assignment(conn, str(mentor.id), str(learner.id))
    print(f"Linked mentor {mentor.email} -> learner {learner.email}.")


if __name__ == "__main__":
    main()
