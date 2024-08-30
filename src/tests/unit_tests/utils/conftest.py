import pytest

from utils.base_models import Base


class ConcreteBase(Base):
    """Concrete model for testing."""

    class Meta:
        app_label = "tests"  # Dummy app label for testing


@pytest.fixture
def base_instance() -> ConcreteBase:
    """Fixture to create a ConcreteBase instance."""
    return ConcreteBase()
