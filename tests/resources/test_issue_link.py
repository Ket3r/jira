from __future__ import annotations
import logging
import pytest

from tests.conftest import JiraTestCase


class _FailOnWarningHandler(logging.Handler):
    def emit(self, record):
        if record.levelno >= logging.WARNING:
            pytest.fail(f"Warning logged during test: {record.getMessage()}")


class IssueLinkTests(JiraTestCase):
    @pytest.fixture(autouse=True)
    def fail_on_log_warning(self):
        # Attach the custom handler to the root logger
        logger = logging.getLogger()
        handler = _FailOnWarningHandler()
        logger.addHandler(handler)
        try:
            yield
        finally:
            # Make sure to remove the handler after the test
            logger.removeHandler(handler)

    def setUp(self):
        JiraTestCase.setUp(self)
        self.link_types = self.test_manager.jira_admin.issue_link_types()

    def test_issue_link(self):
        self.link = self.test_manager.jira_admin.issue_link_type(self.link_types[0].id)
        link = self.link  # Duplicate outward
        self.assertEqual(link.id, self.link_types[0].id)

    def test_create_issue_link(self):
        self.test_manager.jira_admin.create_issue_link(
            self.link_types[0].outward,
            self.test_manager.project_b_issue1,
            self.test_manager.project_b_issue2,
        )

    def test_create_issue_link_with_issue_link_obj(self):
        self.test_manager.jira_admin.create_issue_link(
            self.link_types[0],
            self.test_manager.project_b_issue1,
            self.test_manager.project_b_issue2,
        )

    def test_create_issue_link_with_issue_obj(self):
        inwardissue = self.test_manager.jira_admin.issue(
            self.test_manager.project_b_issue1
        )
        self.assertIsNotNone(inwardissue)
        outwardissue = self.test_manager.jira_admin.issue(
            self.test_manager.project_b_issue2
        )
        self.assertIsNotNone(outwardissue)
        self.test_manager.jira_admin.create_issue_link(
            self.link_types[0].outward, inwardissue, outwardissue
        )

        # @unittest.skip("Creating an issue link doesn't return its ID, so can't easily test delete")
        # def test_delete_issue_link(self):
        #    pass

    def test_issue_link_type(self):
        link_type = self.test_manager.jira_admin.issue_link_type(self.link_types[0].id)
        self.assertEqual(link_type.id, self.link_types[0].id)
        self.assertEqual(link_type.name, self.link_types[0].name)
