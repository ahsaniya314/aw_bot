# Update and Cancel Buttons Fix Plan

## Goal Description

The user reports that the "Update" (btn_update_kirim) and "Cancel" (btn_batal_edit) buttons in the transaction flow are not working. These buttons rely on session state (`sess["action"]`) to determine the next UI step. The current implementation does not reliably set `sess["action"]` to "update_data" when entering update mode, causing the cancel button to fall back to an error message and the update button to not execute the intended update.

## User Review Required

[!IMPORTANT]
Please review the proposed changes, especially the session state handling modifications. Confirm that the approach aligns with the desired behavior.

## Open Questions

- Do we need to support any additional update modes beyond "tambah_cicilan" and "koreksi_data"?
- Should the UI explicitly indicate when the user is in update mode (e.g., update header text) for better UX?

## Proposed Changes

---
### handlers/callback_transaksi.py

- **[MODIFY]** `handle_transaksi_callbacks`:
  - In the branches handling `upd_mode_tambah` and `upd_mode_koreksi`, set `sess["action"] = "update_data"` right after assigning `sess["update_mode"]`.
  - Ensure that after the user confirms the update (`btn_update_kirim`), we also set `sess["action"] = "standby"` (or remove it) to avoid stale state.

- **[MODIFY]** `btn_batal_edit` handling (lines 702-710):
  - Add a fallback to `susun_balasan_resume` when `sess.get("action")` is `None` (treat as input cancel).
  - Update comments to clarify intent.

---
### services/ui_transaksi.py

- **[MODIFY]** `susun_balasan_update`:
  - At the start of the function, set `sess["action"] = "update_data"` to ensure the cancel button knows the context.
  - Ensure the generated markup includes both `btn_update_kirim` and `btn_batal_edit` consistently.

---
### handlers/crud_transaksi.py (if needed)

- Review `tangani_update_status` to confirm it does not rely on the previous `action` value. No changes expected, but verify it returns a proper message.

## Verification Plan

### Automated Tests
- Run existing unit tests (if any) for transaction callbacks.
- Use the `run_command` tool to start the bot in a test environment and simulate callback data for `btn_update_kirim` and `btn_batal_edit`.

### Manual Verification
- Interact with the bot:
  1. Initiate an edit flow (e.g., via `btn_masuk_edit`).
  2. Confirm that the update screen appears and the session `action` is `update_data`.
  3. Press the Cancel button and verify it returns to the previous resume screen.
  4. Press the Update button and verify the transaction is updated.

- Test both update modes (`tambah_cicilan` and `koreksi_data`).

---
