"""Tests for User and Subscription Pydantic models."""

from datetime import datetime
from uuid import UUID

import pytest
from pydantic import ValidationError

from gymnasium_classica.models.user import Plan, Subscription, SubscriptionStatus, User


class TestSubscription:
    """Tests for the Subscription model."""

    def test_defaults(self):
        sub = Subscription()
        assert sub.plan == Plan.FREE
        assert sub.status == SubscriptionStatus.TRIAL
        assert sub.expires_at is None
        assert isinstance(sub.started_at, datetime)

    def test_all_plans(self):
        for plan in ["free", "basic", "premium"]:
            sub = Subscription(plan=plan)
            assert sub.plan == plan

    def test_invalid_plan_rejected(self):
        with pytest.raises(ValidationError):
            Subscription(plan="enterprise")

    def test_all_statuses(self):
        for status in ["trial", "active", "expired"]:
            sub = Subscription(status=status)
            assert sub.status == status

    def test_invalid_status_rejected(self):
        with pytest.raises(ValidationError):
            Subscription(status="cancelled")

    def test_expires_at_can_be_set(self):
        dt = datetime(2027, 6, 1)
        sub = Subscription(expires_at=dt)
        assert sub.expires_at == dt


class TestUser:
    """Tests for the User model."""

    def test_minimal_construction(self):
        user = User(email="test@example.com")
        assert isinstance(user.id, UUID)
        assert user.email == "test@example.com"
        assert user.auth_provider == "local"
        assert isinstance(user.subscription, Subscription)
        assert user.examenjaar_ltc is None
        assert user.examenjaar_gtc is None
        assert isinstance(user.created_at, datetime)

    def test_examenjaar_can_be_set(self):
        user = User(email="test@example.com", examenjaar_ltc=2027, examenjaar_gtc=2028)
        assert user.examenjaar_ltc == 2027
        assert user.examenjaar_gtc == 2028

    def test_custom_subscription(self):
        sub = Subscription(plan="premium", status="active")
        user = User(email="test@example.com", subscription=sub)
        assert user.subscription.plan == Plan.PREMIUM
        assert user.subscription.status == SubscriptionStatus.ACTIVE

    def test_uuid_uniqueness(self):
        user1 = User(email="a@example.com")
        user2 = User(email="b@example.com")
        assert user1.id != user2.id

    def test_serialization_roundtrip(self):
        user = User(email="test@example.com", examenjaar_ltc=2027)
        dumped = user.model_dump()
        user2 = User(**dumped)
        assert user.email == user2.email
        assert user.examenjaar_ltc == user2.examenjaar_ltc
