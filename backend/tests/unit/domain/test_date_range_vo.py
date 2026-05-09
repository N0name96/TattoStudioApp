"""Tests for the DateRange value object.

This module tests the pure business logic of the DateRange value object,
including validation, containment checks, and overlap detection.
"""

from datetime import date, timedelta

import pytest

from domain.value_objects.date_range_vo import DateRange


class TestDateRangeCreation:
    """Tests for DateRange creation and validation."""

    def test_create_date_range_with_valid_dates(self):
        """Test that a DateRange with start before end can be created."""

        start = date(2026, 5, 1)
        end = date(2026, 5, 10)

        date_range = DateRange(start_date=start, end_date=end)

        assert date_range.start_date == start
        assert date_range.end_date == end

    def test_create_date_range_with_same_start_and_end(self):
        """Test that a DateRange with same start and end is valid."""

        single_day = date(2026, 5, 1)

        date_range = DateRange(start_date=single_day, end_date=single_day)

        assert date_range.start_date == single_day
        assert date_range.end_date == single_day

    def test_create_date_range_with_end_before_start_raises_error(self):
        """Test that end_date before start_date raises ValueError."""

        with pytest.raises(ValueError, match="must be on or before end_date"):
            DateRange(start_date=date(2026, 5, 10), end_date=date(2026, 5, 1))


class TestDateRangeContains:
    """Tests for DateRange.contains() method."""

    def test_date_inside_range(self):
        """Test that a date inside the range returns True."""

        date_range = DateRange(
            start_date=date(2026, 5, 1),
            end_date=date(2026, 5, 10),
        )

        assert date_range.contains(date(2026, 5, 5)) is True

    def test_date_at_start_of_range(self):
        """Test that the start_date is considered inside the range."""

        date_range = DateRange(
            start_date=date(2026, 5, 1),
            end_date=date(2026, 5, 10),
        )

        assert date_range.contains(date(2026, 5, 1)) is True

    def test_date_at_end_of_range(self):
        """Test that the end_date is considered inside the range."""

        date_range = DateRange(
            start_date=date(2026, 5, 1),
            end_date=date(2026, 5, 10),
        )

        assert date_range.contains(date(2026, 5, 10)) is True

    def test_date_before_range(self):
        """Test that a date before the range returns False."""

        date_range = DateRange(
            start_date=date(2026, 5, 5),
            end_date=date(2026, 5, 10),
        )

        assert date_range.contains(date(2026, 5, 1)) is False

    def test_date_after_range(self):
        """Test that a date after the range returns False."""

        date_range = DateRange(
            start_date=date(2026, 5, 1),
            end_date=date(2026, 5, 5),
        )

        assert date_range.contains(date(2026, 5, 10)) is False


class TestDateRangeOverlaps:
    """Tests for DateRange.overlaps() method."""

    def test_ranges_that_overlap(self):
        """Test that two overlapping ranges return True."""

        range1 = DateRange(start_date=date(2026, 5, 1), end_date=date(2026, 5, 10))
        range2 = DateRange(start_date=date(2026, 5, 5), end_date=date(2026, 5, 15))

        assert range1.overlaps(range2) is True
        assert range2.overlaps(range1) is True

    def test_adjacent_ranges_touch_at_boundary(self):
        """Test that ranges touching at a boundary overlap."""

        range1 = DateRange(start_date=date(2026, 5, 1), end_date=date(2026, 5, 10))
        range2 = DateRange(start_date=date(2026, 5, 10), end_date=date(2026, 5, 20))

        assert range1.overlaps(range2) is True
        assert range2.overlaps(range1) is True

    def test_ranges_that_do_not_overlap(self):
        """Test that non-overlapping ranges return False."""

        range1 = DateRange(start_date=date(2026, 5, 1), end_date=date(2026, 5, 5))
        range2 = DateRange(start_date=date(2026, 5, 10), end_date=date(2026, 5, 15))

        assert range1.overlaps(range2) is False
        assert range2.overlaps(range1) is False

    def test_range_contained_within_another(self):
        """Test that a range fully inside another overlaps."""

        range1 = DateRange(start_date=date(2026, 5, 1), end_date=date(2026, 5, 30))
        range2 = DateRange(start_date=date(2026, 5, 10), end_date=date(2026, 5, 20))

        assert range1.overlaps(range2) is True
        assert range2.overlaps(range1) is True


class TestDateRangeDuration:
    """Tests for DateRange.duration_days() method."""

    def test_single_day_duration(self):
        """Test that a single day range has duration of 1."""

        today = date.today()
        date_range = DateRange(start_date=today, end_date=today)

        assert date_range.duration_days() == 1

    def test_multi_day_duration(self):
        """Test that a multi-day range calculates correctly."""

        date_range = DateRange(
            start_date=date(2026, 5, 1),
            end_date=date(2026, 5, 10),
        )

        assert date_range.duration_days() == 10

    def test_week_duration(self):
        """Test a full week duration."""

        date_range = DateRange(
            start_date=date(2026, 5, 1),
            end_date=date(2026, 5, 7),
        )

        assert date_range.duration_days() == 7


class TestDateRangeImmutability:
    """Tests for DateRange immutability (frozen dataclass)."""

    def test_date_range_is_immutable(self):
        """Test that DateRange cannot be modified after creation."""

        date_range = DateRange(
            start_date=date(2026, 5, 1),
            end_date=date(2026, 5, 10),
        )

        with pytest.raises(Exception):
            date_range.start_date = date(2026, 6, 1)
