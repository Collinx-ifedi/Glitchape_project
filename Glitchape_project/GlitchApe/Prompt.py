# update the glitchape_central_handler.py to fix order flow and memory:
# 2. Ensure the AI collects customer name, email, phone, address, city, state, zip, and country before checkout.
# 3. Save all order details and variant_id into the session's draft object with proper memory updates after each step.
# 4. After order summary, automatically ask “Are you ready to checkout?” when state becomes 'awaiting_confirmation'.
# 5. Move to 'ready_for_checkout' only after user confirms checkout intent.
# 6. Prevent mockup/product image repetition after product selection; show it only once unless user asks again.
# 7. Add validation to block checkout if variant_id or customer details are missing.
# 8. Improve state transitions: designing → reviewing → awaiting_confirmation → ready_for_checkout → checkout.
# 9. Log memory saves at every new piece of collected info so state is not lost.
# 10. Make the AI respond based on current state instead of free-flow chatting.

# using production level code,update glitchape_central_handler.py and paste the fill production level code. Do not touch anything else not discussed here.