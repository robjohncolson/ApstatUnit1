import re
import os

# --- Configuration ---
INPUT_HTML_FILE = 'index.html'
OUTPUT_HTML_FILE = 'index_modified.html'
UNIT_ID_MARKER_START = "// In Unit "
UNIT_ID_MARKER_END = "'s index.html" # Used to verify we have the right file (optional)

# --- Code Snippets to Inject ---

# Phase 2: JS Bookmark Functions
js_bookmark_functions = r"""
// --- Single Global Bookmark Functions (Supabase) ---

let currentGlobalBookmark = null; // Cache the fetched bookmark state globally within the script

// Fetch the current user's bookmark from Supabase
async function fetchCurrentUserBookmark() {
    // Ensure we have a user ID before querying
    if (!currentUserId) {
         console.log("Fetch Bookmark: No user ID.");
         return null;
    }
    console.log("Fetch Bookmark: Fetching for user ID:", currentUserId);
    try {
        // Select all columns for the user's row (should be max 1 row due to PK)
        const { data, error } = await supabaseClient
            .from('user_bookmarks')
            .select('*')
            .eq('user_id', currentUserId)
            .maybeSingle(); // Use maybeSingle() as the bookmark might not exist

        // Handle potential errors during the fetch
        if (error) {
            console.error('Error fetching bookmark:', error);
            return null; // Return null if there was an error
        }
        // Log success and return the data (bookmark object or null if none found)
        console.log("Fetch Bookmark: Data received:", data);
        return data;
    } catch (err) {
        // Catch any unexpected exceptions during the async operation
        console.error('Exception fetching bookmark:', err);
        return null;
    }
}

// Set or update the user's single bookmark in Supabase (Upsert)
async function setBookmark(unitId, itemId, itemType, itemName, itemUrl) {
    // Check if a user is logged in
    if (!currentUserId) {
        alert('Please identify yourself (enter username) to set a bookmark.');
        return; // Exit if no user
    }

    // Ensure the provided itemUrl is absolute before storing
    let absoluteItemUrl = itemUrl;
    if (itemUrl && !itemUrl.startsWith('http') && !itemUrl.startsWith('#')) {
         // If relative path (e.g., 'pdfs/unit1/file.pdf'), make it absolute based on current page
         absoluteItemUrl = new URL(itemUrl, window.location.href).href;
     } else if (itemUrl && itemUrl.startsWith('#')) {
         // If anchor link (e.g., '#topic-card-1-2'), make it absolute based on current page
         absoluteItemUrl = new URL(itemUrl, window.location.href).href;
     } // Otherwise, assume it's already an absolute URL (http...)

    // Prepare the data object for upserting
    const bookmarkData = {
        user_id: currentUserId, // The primary key, ensures update if exists
        unit_id: unitId,
        item_id: itemId,
        item_type: itemType,
        item_name: itemName,
        item_url: absoluteItemUrl // Store the calculated absolute URL
        // 'updated_at' will be handled by the database trigger or default value
    };

    try {
        console.log('Setting bookmark with data:', bookmarkData);
        // Use upsert: inserts if no row with user_id exists, updates the existing one if it does
        const { data, error } = await supabaseClient // Capture data for immediate update
            .from('user_bookmarks')
            .upsert(bookmarkData, {
                 onConflict: 'user_id', // Specify the constraint/column for conflict resolution
                 // ignoreDuplicates: false // Default is false, meaning it updates on conflict
                 returning: "representation" // Return the inserted/updated row
             })
             .select() // Select the returned representation
             .single(); // Expect a single row back

        // Check for errors during the upsert operation
        if (error) {
            console.error('Error setting bookmark:', error);
            alert('Failed to set bookmark. Please check console and try again.');
        } else {
            console.log('Bookmark set successfully in Supabase.');
            // Update the global cache immediately to reflect the change (use returned data)
            currentGlobalBookmark = data;
            // Refresh the UI indicator and buttons
            await displayGlobalBookmarkIndicator(); // This function now calls updateAllBookmarkButtons internally
        }
    } catch (err) {
        // Catch any unexpected exceptions
        console.error('Exception setting bookmark:', err);
        alert('An error occurred while setting the bookmark.');
    }
}

// Remove the user's bookmark from Supabase
async function removeBookmark() {
    // Ensure user is logged in
    if (!currentUserId) {
        console.log("Remove Bookmark: No user ID.");
        return;
    }

    try {
        console.log('Removing bookmark for user ID:', currentUserId);
        // Delete the row matching the current user's ID
        const { error } = await supabaseClient
            .from('user_bookmarks')
            .delete()
            .eq('user_id', currentUserId); // Target the specific user's row

        // Handle potential deletion errors
        if (error) {
            console.error('Error removing bookmark:', error);
            alert('Failed to remove bookmark. Please check console and try again.');
        } else {
            console.log('Bookmark removed successfully from Supabase.');
            // Clear the global cache
            currentGlobalBookmark = null;
            // Refresh the UI indicator and buttons
            await displayGlobalBookmarkIndicator(); // This function now calls updateAllBookmarkButtons internally
        }
    } catch (err) {
        // Catch any unexpected exceptions
        console.error('Exception removing bookmark:', err);
        alert('An error occurred while removing the bookmark.');
    }
}

 // Updates the appearance of all bookmark buttons on the page
function updateAllBookmarkButtons() {
    // currentGlobalBookmark should be populated by displayGlobalBookmarkIndicator
    console.log("Updating all bookmark buttons based on state:", currentGlobalBookmark);
    document.querySelectorAll('button.bookmark-toggle-btn').forEach(button => {
        const unitId = button.dataset.bookmarkUnit;
        const itemId = button.dataset.bookmarkItem;
        const itemType = button.dataset.bookmarkType;
        let isThisTheBookmark = false;

        if (currentGlobalBookmark && unitId && itemId && itemType) {
            // Compare potentially different types (string from data attribute vs number/string from db)
            isThisTheBookmark = (
                String(currentGlobalBookmark.unit_id) === String(unitId) &&
                String(currentGlobalBookmark.item_id) === String(itemId) &&
                String(currentGlobalBookmark.item_type) === String(itemType)
            );
        }

        const icon = button.querySelector('svg');
        if (isThisTheBookmark) {
            button.classList.add('bookmarked-active');
            button.title = "This is your current bookmark (Click to remove)";
             if (icon) icon.innerHTML = `<path fill-rule="evenodd" d="M5 5a2 2 0 012-2h6a2 2 0 012 2v12l-5-3-5 3V5z" clip-rule="evenodd"></path>`; // Filled Bookmark Icon
             // Use an IIFE or separate function to capture current values for the handler
            (function(currentButton) {
                 currentButton.onclick = (event) => {
                     event.stopPropagation(); // Prevent clicks bubbling up
                     removeBookmark();
                 };
             })(button);

        } else {
            button.classList.remove('bookmarked-active');
            button.title = "Set as Bookmark";
             if (icon) icon.innerHTML = `<path d="M5 4.75C5 3.784 5.784 3 6.75 3h6.5c.966 0 1.75.784 1.75 1.75v13.5a.75.75 0 01-1.227.548L10 15.56l-3.773 2.288A.75.75 0 015 17.25V4.75zm1.75-.25a.25.25 0 00-.25.25v11.462l3.023-1.833a.75.75 0 01.69-.001L13.25 16.21V4.75a.25.25 0 00-.25-.25h-6.5z"></path>`; // Outlined Bookmark Icon
             // Restore onclick to SET bookmark, ensure data attributes are read correctly inside handler
             (function(currentButton, uId, iId, iType, iName, iUrl) {
                  currentButton.onclick = (event) => {
                      event.stopPropagation();
                      setBookmark(uId, iId, iType, iName, iUrl); // Pass original URL
                  };
              })(button, unitId, itemId, itemType, button.dataset.bookmarkName, button.dataset.bookmarkUrl);
        }
    });
}


// Display the global bookmark indicator UI element
async function displayGlobalBookmarkIndicator() {
    const indicator = document.getElementById('global-bookmark-indicator');
    if (!indicator) return; // Ensure the element exists

    if (!currentUserId) {
        indicator.innerHTML = ''; // Hide if no user
        indicator.style.display = 'none';
        currentGlobalBookmark = null;
        // Update buttons even if no user (to show outlined state)
        updateAllBookmarkButtons();
        return;
    }

    indicator.innerHTML = '<span class="text-xs text-gray-500">Loading bookmark...</span>';
    indicator.style.display = 'block'; // Show while loading

    // Fetch (don't necessarily re-fetch if already cached, unless forced)
    // For simplicity on load, always fetch. Could optimize later.
    currentGlobalBookmark = await fetchCurrentUserBookmark(); // Fetch and update cache

    if (currentGlobalBookmark) {
        // URL is already absolute from Supabase
        const jumpUrl = currentGlobalBookmark.item_url;
        const jumpTarget = '_blank'; // Sensible default for external links or different pages

        // Check if the jump URL points to the *current* page's base URL + an anchor
        let isAnchorLink = false;
        try {
             const currentBaseUrl = window.location.origin + window.location.pathname;
             const bookmarkUrlObj = new URL(jumpUrl);
             const bookmarkBaseUrl = bookmarkUrlObj.origin + bookmarkUrlObj.pathname;
             if (bookmarkBaseUrl === currentBaseUrl && bookmarkUrlObj.hash) {
                 isAnchorLink = true;
             }
        } catch(e) { /* Ignore URL parsing errors */ }

        const finalJumpTarget = isAnchorLink ? '_self' : jumpTarget; // Use _self for anchors

        indicator.innerHTML = `
            <div class="bg-yellow-100 border border-yellow-300 text-yellow-800 text-sm p-2 rounded-md shadow flex items-center justify-between gap-2">
                <div class="flex items-center gap-1 overflow-hidden">
                   <svg class="w-4 h-4 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5 5a2 2 0 012-2h6a2 2 0 012 2v12l-5-3-5 3V5z" clip-rule="evenodd"></path></svg>
                   <span class="font-medium flex-shrink-0">Bookmark:</span>
                   <span class="truncate" title="${currentGlobalBookmark.item_name}">
                       ${currentGlobalBookmark.item_name} (Unit ${currentGlobalBookmark.unit_id})
                   </span>
                </div>
                <div class="flex items-center gap-1 flex-shrink-0">
                   <a href="${jumpUrl}" target="${finalJumpTarget}" class="px-1.5 py-0.5 bg-yellow-500 hover:bg-yellow-600 text-white text-xs rounded" title="Jump to Bookmark">Go</a>
                   <button onclick="removeBookmark()" class="px-1.5 py-0.5 bg-yellow-200 hover:bg-yellow-300 text-yellow-900 text-xs rounded" title="Clear Bookmark">Clear</button>
                </div>
            </div>
        `;
         indicator.style.display = 'block'; // Ensure visible
    } else {
        indicator.innerHTML = ''; // Clear if no bookmark
        indicator.style.display = 'none';
    }

    // Update buttons AFTER fetching/updating the global bookmark state
    updateAllBookmarkButtons();
}

// --- End Single Global Bookmark Functions ---
"""

# Phase 3: HTML Indicator Element
html_indicator_div = r"""
    <!-- START Bookmark Indicator Placeholder -->
    <div id="global-bookmark-indicator" class="fixed top-2 right-2 z-50 max-w-xs sm:max-w-sm md:max-w-md lg:max-w-lg xl:max-w-xl print:hidden" style="display: none;">
        <!-- Content injected by displayGlobalBookmarkIndicator() JavaScript function -->
    </div>
    <!-- END Bookmark Indicator Placeholder -->
"""

# Phase 4: CSS Styles
css_styles = r"""
        /* ****** Phase 4: Add Styles for Bookmark Button ****** */
        .bookmark-toggle-btn.bookmarked-active svg {
            color: #f59e0b; /* amber-500 */
        }
        .bookmark-toggle-btn:hover svg {
             color: #3b82f6; /* blue-500 */
         }
        .bookmark-toggle-btn.bookmarked-active:hover svg {
             color: #dc2626; /* red-600 for removing */
         }
        /* Prevent text selection on double click for buttons */
        .bookmark-toggle-btn, #global-bookmark-indicator button, #global-bookmark-indicator a {
             user-select: none;
             -webkit-user-select: none; /* Safari */
             -moz-user-select: none; /* Firefox */
             -ms-user-select: none; /* IE10+ */
         }
"""

# Phase 4: Bookmark Button HTML Template (as a Python string)
# Note the use of backticks ` which need to be escaped in the Python string literal using \`
bookmark_button_template = r"""
                                <!-- Bookmark Button -->
                                <button
                                    class="p-1 ml-2 text-gray-400 hover:text-blue-600 bookmark-toggle-btn flex-shrink-0"
                                    title="Set as Bookmark"
                                    data-bookmark-unit="${UNIT_ID}"
                                    data-bookmark-item="${itemId}"
                                    data-bookmark-type="${itemType}"
                                    data-bookmark-name="${bookmarkName}"
                                    data-bookmark-url="${itemUrl}">
                                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                        <path d="M5 4.75C5 3.784 5.784 3 6.75 3h6.5c.966 0 1.75.784 1.75 1.75v13.5a.75.75 0 01-1.227.548L10 15.56l-3.773 2.288A.75.75 0 015 17.25V4.75zm1.75-.25a.25.25 0 00-.25.25v11.462l3.023-1.833a.75.75 0 01.69-.001L13.25 16.21V4.75a.25.25 0 00-.25-.25h-6.5z"></path>
                                    </svg>
                                </button>
"""

# Phase 5: DOMContentLoaded modifications
dom_load_indicator_call = "        await displayGlobalBookmarkIndicator(); // Load and display early\n"
dom_load_update_buttons_call = "        updateAllBookmarkButtons(); // Update buttons AFTER rendering\n"

# --- Helper Functions ---
def insert_after_marker(content, marker, text_to_insert, first_occurrence=True):
    """Inserts text after the first or all occurrences of a marker."""
    if first_occurrence:
        idx = content.find(marker)
        if idx != -1:
            insert_point = idx + len(marker)
            return content[:insert_point] + text_to_insert + content[insert_point:]
        else:
            print(f"Warning: Marker not found for insertion: {marker}")
            return content
    else:
        # This part is trickier if multiple insertions are needed relative to the marker
        # For this script, we primarily use first_occurrence=True
        return content.replace(marker, marker + text_to_insert)

def insert_before_marker(content, marker, text_to_insert):
    """Inserts text before the first occurrence of a marker."""
    idx = content.find(marker)
    if idx != -1:
        return content[:idx] + text_to_insert + content[idx:]
    else:
        print(f"Warning: Marker not found for insertion: {marker}")
        return content

def modify_card_function(content, function_name_start, button_template):
    """
    Attempts to inject bookmark buttons into JS functions generating cards.
    This is complex and relies on specific string patterns.
    """
    print(f"Attempting to modify function starting with: {function_name_start}")
    # Find the function block roughly
    func_start_idx = content.find(function_name_start)
    if func_start_idx == -1:
        print(f"Warning: Could not find function: {function_name_start}")
        return content

    # Find the likely end of the function (heuristic: next function or end script)
    next_func_idx = content.find("function ", func_start_idx + 1)
    end_script_idx = content.find("</script>", func_start_idx)
    func_end_idx = -1
    if next_func_idx != -1 and end_script_idx != -1:
         func_end_idx = min(next_func_idx, end_script_idx)
    elif next_func_idx != -1:
         func_end_idx = next_func_idx
    elif end_script_idx != -1:
         func_end_idx = end_script_idx

    if func_end_idx == -1:
        print(f"Warning: Could not determine end for function: {function_name_start}")
        return content # Give up if end not found

    function_content = content[func_start_idx:func_end_idx]
    modified_function_content = function_content

    # Regex to find <a> tags for quizzes and videos within the generated HTML strings
    # This looks for the closing </a> tag likely associated with a quiz/video link
    # and inserts the button template *before* the closing </div> of its immediate parent.
    # Pattern: Finds (<a ... href="...(?:pdf|collegeboard|drive)..." ...>...</a>) possibly followed by whitespace, then (</div>)
    # It captures group 1 (the link) and group 2 (the closing div)

    # Modify Quiz Links (both questions and answers if pattern matches)
    # Needs refinement to handle variables inside the JS template literal correctly
    quiz_link_pattern = re.compile(r'(<a.*?href="[^"]*(?:quiz|answers)\.pdf"[^>]*?>.*?</a>\s*)(\n*\s*</div>)', re.DOTALL | re.IGNORECASE)
    def replace_quiz_link(match):
        link_tag = match.group(1)
        closing_div = match.group(2)
        # --- Determine variables needed for the button template ---
        # This part is HARD without parsing JS. We need to assume variables
        # like itemId, itemType, bookmarkName, itemUrl are defined *in the JS scope*
        # where this HTML string is created.
        # We inject JS code that USES those runtime variables.
        # NOTE: The itemId, bookmarkName calculation logic needs to be *inside the JS function already*
        # This Python script just inserts the button template that USES those JS variables.
        # We assume itemType is 'quiz'. itemId and bookmarkName depend on whether it's question/answer.
        # itemUrl is the href from the link_tag (requires parsing the href out or assuming it's in a variable)

        # Simplified: Assume JS variables are correctly named in scope.
        # Need separate logic for question vs answer based on context if possible.
        # For now, using generic placeholders - relies on JS having these defined correctly.
        # A better approach might involve more complex JS injection.
        injected_button = button_template.replace('"${itemId}"', '${quizItemId || answerItemId}') \
                                         .replace('"${itemType}"', "'quiz'") \
                                         .replace('"${bookmarkName}"', '${questionBookmarkName || answerBookmarkName}') \
                                         .replace('"${itemUrl}"', '${quiz.questionPdf || quiz.answersPdf}')

        return link_tag + "\n" + injected_button + closing_div

    modified_function_content = quiz_link_pattern.sub(replace_quiz_link, modified_function_content)


    # Modify Video Links
    video_link_pattern = re.compile(r'(<a.*?href="[^"]*(?:collegeboard|drive\.google)[^"]*"[^>]*?>.*?</a>\s*)(\n*\s*</div>)', re.DOTALL | re.IGNORECASE)
    def replace_video_link(match):
        link_tag = match.group(1)
        closing_div = match.group(2)
        # Assume JS variables videoItemId, videoBookmarkName, videoUrl are defined in scope
        injected_button = button_template.replace('"${itemId}"', '${videoItemId}') \
                                         .replace('"${itemType}"', "'video'") \
                                         .replace('"${bookmarkName}"', '${videoBookmarkName}') \
                                         .replace('"${itemUrl}"', '${videoUrl}')
        return link_tag + "\n" + injected_button + closing_div

    modified_function_content = video_link_pattern.sub(replace_video_link, modified_function_content)

    # Replace original function block with modified one
    if function_content != modified_function_content:
         print(f"Successfully modified function: {function_name_start}")
         return content[:func_start_idx] + modified_function_content + content[func_end_idx:]
    else:
         print(f"Note: No link patterns found or modified in function: {function_name_start}")
         return content


# --- Main Script ---
if __name__ == "__main__":
    if not os.path.exists(INPUT_HTML_FILE):
        print(f"Error: Input file '{INPUT_HTML_FILE}' not found.")
        exit(1)

    print(f"Reading input file: {INPUT_HTML_FILE}")
    with open(INPUT_HTML_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()

    original_length = len(html_content)
    print("Applying modifications...")

    # Optional: Verify Unit ID
    unit_id_start_idx = html_content.find(UNIT_ID_MARKER_START)
    if unit_id_start_idx != -1:
        unit_id_end_idx = html_content.find(UNIT_ID_MARKER_END, unit_id_start_idx)
        if unit_id_end_idx != -1:
             detected_unit = html_content[unit_id_start_idx + len(UNIT_ID_MARKER_START) : unit_id_end_idx].strip()
             print(f"Detected Unit ID comment: {detected_unit}")
             # Add more checks if needed
        else:
             print("Warning: Could not find end marker for Unit ID comment.")
    else:
        print("Warning: Could not find start marker for Unit ID comment.")


    # Phase 2: Inject JS Functions
    js_anchor = "// Global user variables"
    html_content = insert_before_marker(html_content, js_anchor, js_bookmark_functions + "\n\n")
    if len(html_content) == original_length: print("JS Functions potentially not added.")
    else: print(" -> JS Bookmark functions added.")

    # Phase 3: Inject HTML Indicator Div
    html_anchor = '<div class="container mx-auto px-4 py-8">'
    # Make sure not to insert multiple times if script is run again
    if '<div id="global-bookmark-indicator"' not in html_content:
        html_content = insert_after_marker(html_content, html_anchor, "\n" + html_indicator_div)
        if len(html_content) == original_length: print("HTML Indicator potentially not added.")
        else: print(" -> HTML Indicator div added.")
    else:
        print(" -> HTML Indicator div already present, skipped.")


    # Phase 4: Inject CSS Styles
    css_anchor = "</style>"
    # Make sure not to insert multiple times
    if ".bookmark-toggle-btn" not in html_content:
         html_content = insert_before_marker(html_content, css_anchor, css_styles + "\n    ")
         if len(html_content) == original_length: print("CSS styles potentially not added.")
         else: print(" -> CSS Bookmark styles added.")
    else:
        print(" -> CSS Bookmark styles already present, skipped.")


    # Phase 4: Inject Bookmark Buttons into Card Functions (Complex)
    # WARNING: This regex modification is FRAGILE. Manual verification is needed.
    # It modifies the JS code strings.
    print("Attempting complex modifications for bookmark buttons...")
    html_content_before_buttons = html_content
    html_content = modify_card_function(html_content, "function createTopicCard", bookmark_button_template)
    html_content = modify_card_function(html_content, "function updateCurrentTopicInfo", bookmark_button_template)
    html_content = modify_card_function(html_content, "function populateQuickAccessTopics", bookmark_button_template)
    if len(html_content) == len(html_content_before_buttons):
         print("Warning: No button templates seem to have been injected. Check modification logic/patterns.")


    # Phase 5: Modify DOMContentLoaded
    print("Modifying DOMContentLoaded...")
    dom_content_marker = "document.addEventListener('DOMContentLoaded', async function() {"
    dom_content_start_idx = html_content.find(dom_content_marker)

    if dom_content_start_idx != -1:
        # Add indicator call after identifyUser
        identify_user_call = "await identifyUser();"
        if dom_load_indicator_call.strip() not in html_content:
             html_content = insert_after_marker(html_content, identify_user_call, "\n\n    " + dom_load_indicator_call)
             print(" -> Added displayGlobalBookmarkIndicator call.")
        else:
             print(" -> displayGlobalBookmarkIndicator call already present.")

        # Add update buttons call after card population calls
        card_render_calls = [
            "populateTopicCards();",
            "updateCurrentTopicInfo();",
            "populateQuickAccessTopics();"
        ]
        modified_dom_content = False
        for call in card_render_calls:
            # Find all occurrences of the call within DOMContentLoaded
             start_search = dom_content_start_idx
             while True:
                 idx = html_content.find(call, start_search)
                 if idx == -1 or idx > html_content.find("});", dom_content_start_idx): # Ensure within DOMContentLoaded block
                     break
                 insert_point = idx + len(call)
                 # Check if the update call is already immediately after
                 if html_content[insert_point:].lstrip().startswith(dom_load_update_buttons_call.strip()):
                     start_search = insert_point # Move past existing call
                     continue
                 # Insert the update call
                 html_content = html_content[:insert_point] + "\n" + dom_load_update_buttons_call + html_content[insert_point:]
                 modified_dom_content = True
                 start_search = insert_point + len(dom_load_update_buttons_call) + 1 # Move search past inserted text

        if modified_dom_content:
             print(" -> Added updateAllBookmarkButtons calls.")
        else:
             print(" -> updateAllBookmarkButtons calls seemed present or render calls not found.")

    else:
        print("Warning: DOMContentLoaded listener not found.")

    # --- Output ---
    print(f"Writing modified content to: {OUTPUT_HTML_FILE}")
    with open(OUTPUT_HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("-" * 20)
    print("Script finished.")
    print(f"Please manually review '{OUTPUT_HTML_FILE}' carefully, especially the modifications within the JavaScript functions for button injection, before replacing your original file.")
    print("-" * 20)