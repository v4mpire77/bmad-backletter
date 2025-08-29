import time
from playwright.sync_api import sync_playwright, Page, expect

def test_export_dialog_a11y(page: Page):
    print("Testing ExportDialog accessibility...")
    page.goto("http://localhost:3000/analyses/mock-1")
    page.get_by_role("button", name="Export").click()

    dialog = page.get_by_role("dialog", name="Export Report")
    expect(dialog).to_be_visible()

    # Test focus trap
    close_button = dialog.get_by_role("button", name="Close export dialog")
    expect(close_button).to_be_focused()

    page.keyboard.press("Tab")
    include_logo_checkbox = page.get_by_label("Include logo")
    expect(include_logo_checkbox).to_be_focused()

    page.keyboard.press("Tab")
    include_meta_checkbox = page.get_by_label("Include metadata (filename, checksum)")
    expect(include_meta_checkbox).to_be_focused()

    page.keyboard.press("Tab")
    date_format_select = page.get_by_label("Date format")
    expect(date_format_select).to_be_focused()

    page.keyboard.press("Tab")
    cancel_button = dialog.get_by_role("button", name="Cancel")
    expect(cancel_button).to_be_focused()

    page.keyboard.press("Tab")
    export_button = dialog.get_by_role("button", name="Export (preview)")
    expect(export_button).to_be_focused()

    # Test focus wrap forward
    page.keyboard.press("Tab")
    expect(close_button).to_be_focused()

    # Test focus wrap backward
    page.keyboard.press("Shift+Tab")
    expect(export_button).to_be_focused()

    # Test Escape key
    page.keyboard.press("Escape")
    expect(dialog).not_to_be_visible()
    print("ExportDialog accessibility test passed.")


def test_evidence_drawer_a11y(page: Page):
    print("Testing EvidenceDrawer accessibility...")
    page.goto("http://localhost:3000/analyses/mock-1")

    # Open the drawer
    page.get_by_role("button", name="View").first.click()

    drawer = page.get_by_role("dialog", name="evidence-title")
    expect(drawer).to_be_visible()

    # Test focus trap
    close_button = drawer.get_by_role("button", name="Close")
    expect(close_button).to_be_focused()

    page.keyboard.press("Tab")
    copy_button = drawer.get_by_role("button", name="Copy snippet")
    expect(copy_button).to_be_focused()

    # This button may or may not be present
    mark_reviewed_button = drawer.get_by_role("button", name="Mark reviewed")
    if mark_reviewed_button.is_visible():
        page.keyboard.press("Tab")
        expect(mark_reviewed_button).to_be_focused()

    # Test focus wrap forward
    page.keyboard.press("Tab")
    expect(close_button).to_be_focused()

    # Test focus wrap backward
    page.keyboard.press("Shift+Tab")
    if mark_reviewed_button.is_visible():
        expect(mark_reviewed_button).to_be_focused()
    else:
        expect(copy_button).to_be_focused()

    # Test Escape key
    page.keyboard.press("Escape")
    expect(drawer).not_to_be_visible()
    print("EvidenceDrawer accessibility test passed.")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        test_export_dialog_a11y(page)
        page.screenshot(path="jules-scratch/verification/export-dialog-test.png")

        # Give a moment for the page to reset
        time.sleep(1)

        test_evidence_drawer_a11y(page)
        page.screenshot(path="jules-scratch/verification/evidence-drawer-test.png")

        browser.close()
    print("All accessibility verification tests passed.")

if __name__ == "__main__":
    main()
