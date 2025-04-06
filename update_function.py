#!/usr/bin/env python3

import re
import sys

def update_file(file_path):
    try:
        # Read the entire file content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # New function implementation to replace the old one
        new_function = '''
        // Function to check if daily quota has been met and record it in Supabase
        async function checkDailyQuotaCompletion() {
            // Check if currentUserId exists
            if (!currentUserId) {
                console.log('DEBUG: Cannot check daily quota without user ID.');
                return;
            }
            
            // Calculate flexible targets
            let requiredVideosPerDay = 5; // Default fallback
            let requiredQuizzesPerDay = 3; // Default fallback
            
            try {
                // Get total counts and calculate days remaining
                if (typeof ALL_UNITS_DATA !== 'undefined' && Array.isArray(ALL_UNITS_DATA)) {
                    const { totalVideos, totalQuizzes } = getTotalItemCounts(ALL_UNITS_DATA);
                    
                    // Calculate days remaining until May 8th, 2025 (AP Statistics Exam date)
                    const today = new Date();
                    const examDate = new Date('May 8, 2025');
                    
                    if (today <= examDate) {
                        const timeDiff = examDate.getTime() - today.getTime();
                        const daysRemaining = Math.ceil(timeDiff / (1000 * 3600 * 24));
                        
                        requiredVideosPerDay = Math.ceil(totalVideos / daysRemaining);
                        requiredQuizzesPerDay = Math.ceil(totalQuizzes / daysRemaining);
                        
                        console.log(`DEBUG: Calculated flexible targets: ${requiredVideosPerDay} videos, ${requiredQuizzesPerDay} quizzes per day.`);
                    }
                } else {
                    console.log('DEBUG: ALL_UNITS_DATA not available, using default targets.');
                }
            } catch (error) {
                console.error('Error calculating flexible targets:', error);
                // Continue with default values
            }
            
            // Get today's date boundaries
            const now = new Date();
            const startOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 0, 0, 0).toISOString();
            const endOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 23, 59, 59).toISOString();
            const todayDateString = now.toISOString().split('T')[0]; // YYYY-MM-DD format
            
            console.log(`DEBUG: Checking completions for ${todayDateString} from ${startOfDay} to ${endOfDay}`);
            
            try {
                // Query Supabase for today's completions
                const { data, error } = await supabaseClient
                    .from('completions')
                    .select('item_type')
                    .eq('user_id', currentUserId)
                    .gte('completed_at', startOfDay)
                    .lte('completed_at', endOfDay);
                
                if (error) {
                    console.error('Error fetching today\\'s completions:', error);
                    return;
                }
                
                // Count videos and quizzes completed today
                const videosToday = data ? data.filter(item => item.item_type === 'video').length : 0;
                const quizzesToday = data ? data.filter(item => item.item_type === 'quiz').length : 0;
                
                console.log(`DEBUG: Today's completions: ${videosToday} videos, ${quizzesToday} quizzes.`);
                console.log(`DEBUG: Required: ${requiredVideosPerDay} videos, ${requiredQuizzesPerDay} quizzes.`);
                
                // Check if quota is met
                if (videosToday >= requiredVideosPerDay && quizzesToday >= requiredQuizzesPerDay) {
                    console.log('DEBUG: Daily flexible quota requirements met!');
                    
                    // Record in Supabase daily_quotas_met table
                    const { error: insertError } = await supabaseClient
                        .from('daily_quotas_met')
                        .insert({
                            user_id: currentUserId,
                            quota_date: todayDateString
                        });
                    
                    if (!insertError) {
                        console.log('DEBUG: Daily flexible quota met and logged.');
                        
                        // Optional: Add a subtle notification here
                        // For example, briefly show a success message or update an icon
                        
                    } else if (insertError.code === '23505') {
                        // This is a unique violation error (quota already logged for today)
                        console.log('DEBUG: Quota already logged for today.');
                    } else {
                        console.error('Error logging quota completion:', insertError);
                    }
                } else {
                    console.log('DEBUG: Daily quota not yet met.');
                }
            } catch (error) {
                console.error('Error during quota check process:', error);
            }
        }'''
        
        # Replace old function definition
        pattern = r'\/\/ Placeholder function for checking local storage quota\s+function checkLocalQuota\(\) \{\s+\/\/ This function will be implemented later\s+console\.log\(\'Local storage quota check placeholder\'\);\s+\}'
        
        if re.search(pattern, content, re.DOTALL):
            modified_content = re.sub(pattern, new_function, content, flags=re.DOTALL)
            # Replace function calls
            modified_content = modified_content.replace('checkLocalQuota();', 'checkDailyQuotaCompletion();')
            
            # Save the modified content back to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(modified_content)
            
            print(f"SUCCESS: Replaced the function and all its references in {file_path}")
            return True
        else:
            print(f"ERROR: Could not find the checkLocalQuota function definition pattern in {file_path}")
            return False
        
    except Exception as e:
        print(f"ERROR: An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "index.html"  # Default path
    
    update_file(file_path)