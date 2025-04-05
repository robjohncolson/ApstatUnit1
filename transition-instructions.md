Okay, let's get Unit 1 connected to Supabase! We'll add the necessary code to save progress online and identify the user.

**Phase 2: Minimal Supabase Integration (Unit 1)**

*(You should be working within the `index.html` file for Unit 1 in your Cursor IDE)*

1.  **Add Supabase SDK:**
    *   **Action:** Ask Claude in Cursor:
        ```cursor-prompt
        In the `<head>` section of this `index.html` file, please add the necessary `<script>` tag to include the Supabase V2 Javascript SDK from its CDN.
        ```
    *   **Verify:** Claude should add a line like this inside the `<head>` tags:
        ```html
        <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
        ```
        *(Make sure it's there before proceeding)*

2.  **Initialize Supabase Client:**
    *   **Action:** Go to the *very beginning* of your main `<script>` block (likely right after `<script>`). Ask Claude:
        ```cursor-prompt
        At the top of this script block, before any function definitions, please add the code to initialize the Supabase client using constants `SUPABASE_URL` and `SUPABASE_ANON_KEY`. Use placeholder values for now. Also, declare global variables `currentUsername` and `currentUserId`, both initialized to `null`.
        ```
    *   **Verify & Edit:** Claude should add something like this:
        ```javascript
        const SUPABASE_URL = 'YOUR_SUPABASE_URL'; // <<< EDIT THIS LINE
        const SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_KEY'; // <<< EDIT THIS LINE
        const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

        let currentUsername = null;
        let currentUserId = null;
        ```
    *   **ACTION:** **Manually replace** `'YOUR_SUPABASE_URL'` and `'YOUR_SUPABASE_ANON_KEY'` with the actual **URL** and **anon public key** you copied from your Supabase project settings (Phase 0, Step 4). **Be careful not to paste the service_role key!**

3.  **Implement User Identification:**
    *   **Action:** Ask Claude:
        ```cursor-prompt
        Please create an `async` function called `identifyUser`. This function should perform the following steps:
        1. Get 'apStatsUsername' and 'apStatsUserId' from `localStorage` and assign them to the global `currentUsername` and `currentUserId` variables.
        2. Check if `currentUsername` is null or empty. If it is:
            a. Use `prompt("Enter your username (visible to others):")` to ask the user for their username.
            b. If the user cancels or enters nothing, log a warning and return early (do nothing else).
            c. Store the entered username in `localStorage` under the key 'apStatsUsername' and assign it to `currentUsername`.
            d. Set `currentUserId` to `null` and remove 'apStatsUserId' from localStorage (to force a database lookup/create).
        3. Check if `currentUsername` has a value AND `currentUserId` is null. If both are true:
            a. Start a `try...catch` block for Supabase operations.
            b. Inside the `try`, use `await supabase.from('users').select('id').eq('username', currentUsername).maybeSingle()` to check if the user exists in the database. Store the result.
            c. If the query has an error (other than 'Row not found'), throw the error.
            d. If the query result contains a user (`result.data` is not null), assign `result.data.id` to `currentUserId`.
            e. If the query result is null (user not found), use `await supabase.from('users').insert({ username: currentUsername }).select().single()` to create the user. If there's an insert error, throw it. Assign the new user's `id` from the insert result to `currentUserId`.
            e. If `currentUserId` now has a value, store it in `localStorage` under the key 'apStatsUserId'.
            f. Log the identified/created username and ID to the console.
            g. In the `catch` block, log the error to the console, show an `alert('Could not connect to online progress tracker. Progress will only be saved locally.')`, and ensure `currentUserId` is set back to `null`.
        ```
    *   **Verify:** Read through the function Claude generates. Does it match the logic described? Does it handle errors?

4.  **Call `identifyUser()` on Load:**
    *   **Action:** Find your `DOMContentLoaded` event listener (it probably contains calls to `loadTopicProgress`, `populateTopicCards`, etc.). Ask Claude:
        ```cursor-prompt
        Inside the `DOMContentLoaded` event listener, right at the beginning before any other function calls like `loadTopicProgress`, add a line to call `await identifyUser();`. Ensure the listener itself is marked as `async`.
        ```
    *   **Verify:** Check that the listener now looks something like:
        ```javascript
        document.addEventListener('DOMContentLoaded', async () => { // <--- Added async
            await identifyUser(); // <--- Added this call
            loadTopicProgress();
            populateTopicCards();
            // ... other initial setup calls ...
        });
        ```

5.  **Implement `saveCompletionToSupabase` Function:**
    *   **Action:** Ask Claude:
        ```cursor-prompt
        Please create an `async` function called `saveCompletionToSupabase` that accepts three arguments: `itemType` (string), `itemIdentifier` (string), and `unitId` (string).
        1. Inside the function, first check if the global `currentUserId` variable is null. If it is, log a warning "No user ID, skipping Supabase save." and `return` immediately.
        2. Use a `try...catch` block.
        3. Inside the `try`, use `await supabase.from('completions').insert({...})` to insert a single record into the 'completions' table. The record object should include:
            - `user_id`: the value of `currentUserId`.
            - `item_type`: the `itemType` argument.
            - `item_identifier`: the `itemIdentifier` argument.
            - `unit_id`: the `unitId` argument.
            - `completed_at`: `new Date().toISOString()`.
        4. If the insert call returns an `error`, throw it.
        5. If successful, log a confirmation message like `Completion saved to Supabase: ${itemType} - ${itemIdentifier}`.
        6. **Crucially:** After a successful save log message, add a call to `checkLocalQuota();` (This function might not exist fully yet, but add the call).
        7. Inside the `catch` block, log the error message to the console (e.g., 'Error saving completion to Supabase:').
        ```
    *   **Verify:** Read the generated function. Does it have the safety check for `currentUserId`? Does it insert the correct fields? Does it call `checkLocalQuota()` *after* success and *before* the catch block?

6.  **Modify Completion Handlers to Call Supabase:**
    *   **Action:** Find the `markVideoComplete` and `markQuizComplete` functions you created in Phase 1. Ask Claude:
        ```cursor-prompt
        Modify the functions `markVideoComplete` and `markQuizComplete`. Inside each function, *after* the line that calls `saveTopicProgress()`:
        1. Add a conditional check: `if (currentUserId) { ... }`.
        2. Inside this `if` block, call the `saveCompletionToSupabase` function.
        3. Pass the correct arguments:
            - For `markVideoComplete`: `saveCompletionToSupabase('video', videoUrl, 'unit1');`
            - For `markQuizComplete`: `saveCompletionToSupabase('quiz', quizId, 'unit1');`
        *(Make sure 'unit1' is correctly passed as the `unitId`)*.
        ```
    *   **Verify:** Check both functions. Is the `saveCompletionToSupabase` call present? Is it *inside* the `if (currentUserId)` check? Is the `unitId` argument hardcoded correctly as `'unit1'`?

7.  **Testing (Crucial Step):**
    *   **Clear Local Storage:** Open Developer Tools (F12), go to Application -> Local Storage, right-click your site's entry, and choose "Clear".
    *   **Reload `index.html`:** Refresh the page.
    *   **User Prompt:** You should be prompted to enter your username. Enter one (e.g., `TestUser1`). Click OK.
    *   **Check Console:** Look for logs from `identifyUser`. Did it find/create the user? Does it log your `currentUserId` (a long string)?
    *   **Check Supabase:** Go to your Supabase project dashboard -> Table Editor -> `users` table. Do you see `TestUser1` listed with a generated `id`?
    *   **Mark Items Complete:** Click the checkbox for a video, then for a quiz.
    *   **Check Console:** Look for logs:
        *   Did `markVideoComplete` / `markQuizComplete` run?
        *   Did `saveCompletionToSupabase` run? Did it log success?
    *   **Check Supabase:** Go to the `completions` table in Supabase. Do you see new rows corresponding to the items you checked? Do they have the correct `user_id`, `item_type`, `item_identifier`, and `unit_id` ('unit1')?
    *   **Reload Again:** Refresh the page.
        *   You should *not* be prompted for a username this time (it's stored locally).
        *   The items you marked should still be checked (loaded from localStorage).
        *   Check the console - `identifyUser` should log that it found the existing user ID from localStorage.
    *   **Test Offline:** Disconnect your computer from the internet (turn off Wi-Fi). Reload the page.
        *   Does the page load? (It should).
        *   Mark another item complete. Does the checkbox update visually? (It should - local update).
        *   Check the console. You should see an error message from `saveCompletionToSupabase` saying it couldn't connect.
    *   **Reconnect:** Turn Wi-Fi back on. Refresh the page. The locally completed item should still be checked, but note that the completion *during the offline period* was likely not saved to Supabase.

You have now completed Phase 2 for Unit 1. The page identifies the user and attempts to save every completion to your Supabase database, while still functioning locally. You can now repeat these Phase 2 steps for Units 2 through 9, remembering to change the hardcoded `unitId` (e.g., `'unit2'`, `'unit3'`) in step 6 for each respective unit file.