"""
Listy - AI Travel Assistant for ListAcross.eu
A friendly, helpful chatbot for European travel recommendations
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from travel.openai_direct import DirectOpenAIClient
import json
import logging

logger = logging.getLogger(__name__)


class ListyAssistant:
    """
    Listy - Your friendly European travel assistant
    """
    
    def __init__(self):
        self.client = DirectOpenAIClient()
        self.personality = """
        You are Listy, a very friendly and enthusiastic AI travel assistant for ListAcross.eu! 
        
        Your personality:
        - Very helpful and sympathetic 
        - Enthusiastic about European travel
        - Always smiling (use emojis!)
        - Knowledgeable about European cities, culture, food, and attractions
        - Give practical, actionable travel advice
        - Keep responses conversational and not too long
        - Always mention that you work for ListAcross.eu when relevant
        
        You help people with:
        - Travel recommendations for European cities
        - Restaurant suggestions
        - Attraction recommendations  
        - Travel tips and cultural insights
        - Budget planning
        - Transportation advice
        
        Always be positive, helpful, and add personality to your responses!
        """
    
    def chat(self, user_message: str, context: dict = None) -> dict:
        """
        Process user message and return Listy's response
        """
        if not self.client.client:
            return {
                'success': False,
                'message': "Hi! I'm Listy! 😊 I'm having some technical difficulties right now, but I'll be back to help you with your European travels soon! 💕"
            }
        
        # Build conversation context
        system_prompt = self.personality
        
        if context and context.get('current_city'):
            system_prompt += f"\n\nContext: The user is currently looking at travel information for {context['current_city']}."
        
        # Add some European travel knowledge
        system_prompt += """
        
        Some key cities I love to help with:
        - Hamburg: Maritime charm, Speicherstadt, vibrant nightlife
        - Barcelona: Gaudi architecture, beach culture, amazing tapas
        - Amsterdam: Canals, museums, bike-friendly culture
        - Vienna: Classical music, coffee houses, imperial architecture
        - Prague: Fairy-tale architecture, cheap beer, historic charm
        - And many more European destinations!
        
        Remember to be enthusiastic and use emojis!
        """
        
        try:
            response = self.client.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=300,  # Keep responses concise
                temperature=0.8  # Make it more conversational
            )
            
            listy_response = response.choices[0].message.content
            
            return {
                'success': True,
                'message': listy_response,
                'personality': 'friendly'
            }
            
        except Exception as e:
            logger.error(f"Listy error: {str(e)}")
            return {
                'success': False,
                'message': "Oops! 😅 I'm having a little trouble right now. But don't worry - I'm Listy and I'm always here to help with your European travels! Try asking me again in a moment! 💕"
            }


@require_POST
@csrf_exempt
def listy_chat(request):
    """
    API endpoint for chatting with Listy
    """
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        context = data.get('context', {})
        
        if not user_message:
            return JsonResponse({
                'success': False,
                'message': "Hi there! I'm Listy! 😊 What would you like to know about traveling in Europe? 🌍"
            })
        
        # Create Listy instance and get response
        listy = ListyAssistant()
        response = listy.chat(user_message, context)
        
        return JsonResponse(response)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': "Hi! I'm Listy! 😊 I didn't quite understand that. Could you try asking me about European travel again? 💕"
        })
    except Exception as e:
        logger.error(f"Listy chat error: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': "Hi! I'm Listy! 😊 Something went wrong, but I'm here to help with your European travel questions! Try again! 🌟"
        })


def listy_widget(request):
    """
    Return the Listy chat widget HTML
    """
    widget_html = """
    <!-- Listy Chat Widget -->
    <div id="listy-widget" style="display: none;">
        <div id="listy-chat-container">
            <div id="listy-header">
                <div class="listy-avatar">😊</div>
                <div class="listy-info">
                    <strong>Listy</strong>
                    <small>Your travel assistant</small>
                </div>
                <button id="listy-minimize">−</button>
            </div>
            
            <div id="listy-messages">
                <div class="listy-message">
                    <div class="listy-avatar-small">😊</div>
                    <div class="message-content">
                        Hi! I'm Listy! 🌍 I'm here to help you discover amazing European destinations! What would you like to know? ✨
                    </div>
                </div>
            </div>
            
            <div id="listy-input-area">
                <input type="text" id="listy-input" placeholder="Ask me about European travel...">
                <button id="listy-send">Send</button>
            </div>
        </div>
    </div>
    
    <style>
        #listy-widget {
            position: fixed;
            bottom: 100px;
            right: 30px;
            width: 350px;
            height: 500px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            z-index: 1001;
            display: flex;
            flex-direction: column;
        }
        
        #listy-header {
            background: linear-gradient(45deg, #ff6b6b, #ffa500);
            color: white;
            padding: 15px;
            border-radius: 15px 15px 0 0;
            display: flex;
            align-items: center;
        }
        
        .listy-avatar {
            font-size: 2rem;
            margin-right: 10px;
        }
        
        .listy-info strong {
            display: block;
            font-size: 1.1rem;
        }
        
        .listy-info small {
            opacity: 0.9;
        }
        
        #listy-minimize {
            margin-left: auto;
            background: transparent;
            border: none;
            color: white;
            font-size: 1.5rem;
            cursor: pointer;
        }
        
        #listy-messages {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            max-height: 350px;
        }
        
        .listy-message {
            display: flex;
            margin-bottom: 15px;
            align-items: flex-start;
        }
        
        .user-message {
            flex-direction: row-reverse;
        }
        
        .listy-avatar-small {
            font-size: 1.5rem;
            margin-right: 8px;
        }
        
        .user-message .listy-avatar-small {
            margin-right: 0;
            margin-left: 8px;
        }
        
        .message-content {
            background: #f0f0f0;
            padding: 10px 12px;
            border-radius: 15px;
            max-width: 80%;
            line-height: 1.4;
        }
        
        .user-message .message-content {
            background: #007bff;
            color: white;
        }
        
        #listy-input-area {
            padding: 15px;
            border-top: 1px solid #eee;
            display: flex;
            gap: 10px;
        }
        
        #listy-input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 20px;
            outline: none;
        }
        
        #listy-send {
            background: linear-gradient(45deg, #ff6b6b, #ffa500);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 20px;
            cursor: pointer;
        }
        
        .typing-indicator {
            display: flex;
            align-items: center;
            gap: 8px;
            opacity: 0.7;
        }
        
        .typing-dots {
            display: flex;
            gap: 3px;
        }
        
        .typing-dots span {
            width: 6px;
            height: 6px;
            background: #999;
            border-radius: 50%;
            animation: typing 1.5s infinite;
        }
        
        .typing-dots span:nth-child(2) { animation-delay: 0.2s; }
        .typing-dots span:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typing {
            0%, 60%, 100% { transform: scale(1); }
            30% { transform: scale(1.2); }
        }
    </style>
    """
    
    return JsonResponse({'widget_html': widget_html})