'use client';

import { useState, useEffect, useRef } from 'react';
import { EU_LANGUAGES } from './LanguageSelector';

interface Message {
    id: string;
    content: string;
    isUser: boolean;
    timestamp: Date;
    language?: string;
}

interface ListyAssistantProps {
    selectedLanguage: string;
    onLanguageChange?: (lang: string) => void;
}

export default function ListyAssistant({ selectedLanguage, onLanguageChange }: ListyAssistantProps) {
    const [messages, setMessages] = useState<Message[]>([]);
    const [inputValue, setInputValue] = useState('');
    const [isOpen, setIsOpen] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [isMinimized, setIsMinimized] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLInputElement>(null);

    const currentLang = EU_LANGUAGES.find(lang => lang.code === selectedLanguage) || EU_LANGUAGES[5];

    // Welcome messages in different languages
    const welcomeMessages: Record<string, string> = {
        'en': "Hi! I'm Listy, your AI assistant for ListAcrossEU! 🇪🇺 I can help you find businesses, translate content, and navigate our directory of 6,331+ European businesses. How can I help you today?",
        'es': "¡Hola! Soy Listy, tu asistente IA para ListAcrossEU! 🇪🇺 Puedo ayudarte a encontrar empresas, traducir contenido y navegar nuestro directorio de más de 6,331 empresas europeas. ¿Cómo puedo ayudarte hoy?",
        'fr': "Salut! Je suis Listy, votre assistant IA pour ListAcrossEU! 🇪🇺 Je peux vous aider à trouver des entreprises, traduire du contenu et naviguer dans notre répertoire de plus de 6,331 entreprises européennes. Comment puis-je vous aider aujourd'hui?",
        'de': "Hallo! Ich bin Listy, Ihr KI-Assistent für ListAcrossEU! 🇪🇺 Ich kann Ihnen helfen, Unternehmen zu finden, Inhalte zu übersetzen und in unserem Verzeichnis von über 6,331 europäischen Unternehmen zu navigieren. Wie kann ich Ihnen heute helfen?",
        'it': "Ciao! Sono Listy, il tuo assistente IA per ListAcrossEU! 🇪🇺 Posso aiutarti a trovare aziende, tradurre contenuti e navigare nella nostra directory di oltre 6,331 aziende europee. Come posso aiutarti oggi?",
        'pt': "Olá! Sou Listy, seu assistente IA para ListAcrossEU! 🇪🇺 Posso ajudá-lo a encontrar empresas, traduzir conteúdo e navegar em nosso diretório de mais de 6,331 empresas europeias. Como posso ajudá-lo hoje?",
        'nl': "Hallo! Ik ben Listy, je AI-assistent voor ListAcrossEU! 🇪🇺 Ik kan je helpen bedrijven te vinden, content te vertalen en door ons directory van 6,331+ Europese bedrijven te navigeren. Hoe kan ik je vandaag helpen?"
    };

    // Quick action suggestions
    const quickActions: Record<string, string[]> = {
        'en': [
            "🔍 Find restaurants in Madrid",
            "🏢 Show German businesses",
            "🌍 List all countries",
            "📊 Platform statistics",
            "🇪🇺 Change language"
        ],
        'es': [
            "🔍 Buscar restaurantes en Madrid",
            "🏢 Mostrar empresas alemanas",
            "🌍 Listar todos los países",
            "📊 Estadísticas de la plataforma",
            "🇪🇺 Cambiar idioma"
        ],
        'fr': [
            "🔍 Trouver restaurants à Madrid",
            "🏢 Voir entreprises allemandes",
            "🌍 Lister tous les pays",
            "📊 Statistiques plateforme",
            "🇪🇺 Changer langue"
        ],
        'de': [
            "🔍 Restaurants in Madrid finden",
            "🏢 Deutsche Unternehmen zeigen",
            "🌍 Alle Länder auflisten",
            "📊 Plattform-Statistiken",
            "🇪🇺 Sprache ändern"
        ]
    };

    useEffect(() => {
        if (messages.length === 0) {
            const welcomeMsg = welcomeMessages[selectedLanguage] || welcomeMessages['en'];
            setMessages([{
                id: '1',
                content: welcomeMsg,
                isUser: false,
                timestamp: new Date(),
                language: selectedLanguage
            }]);
        }
    }, [selectedLanguage]);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const handleSendMessage = async () => {
        if (!inputValue.trim()) return;

        const userMessage: Message = {
            id: Date.now().toString(),
            content: inputValue,
            isUser: true,
            timestamp: new Date(),
            language: selectedLanguage
        };

        setMessages(prev => [...prev, userMessage]);
        setInputValue('');
        setIsLoading(true);

        try {
            // Simulate AI response (replace with actual API call)
            const response = await simulateListyResponse(inputValue, selectedLanguage);

            const assistantMessage: Message = {
                id: (Date.now() + 1).toString(),
                content: response,
                isUser: false,
                timestamp: new Date(),
                language: selectedLanguage
            };

            setMessages(prev => [...prev, assistantMessage]);
        } catch (error) {
            console.error('Error getting Listy response:', error);
            const errorMsg = getErrorMessage(selectedLanguage);
            const assistantMessage: Message = {
                id: (Date.now() + 1).toString(),
                content: errorMsg,
                isUser: false,
                timestamp: new Date(),
                language: selectedLanguage
            };
            setMessages(prev => [...prev, assistantMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const simulateListyResponse = async (input: string, lang: string): Promise<string> => {
        try {
            // Try to call the real API first
            const response = await fetch('/api/listy/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: input,
                    language: lang
                })
            });

            if (response.ok) {
                const data = await response.json();
                return data.response;
            }
        } catch (error) {
            console.log('API not available, using fallback responses');
        }

        // Fallback to simulated responses if API is not available
        await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 1000));
        const lowerInput = input.toLowerCase();

        // Language-specific responses
        const responses: Record<string, Record<string, string>> = {
            'en': {
                'businesses': "I found your business data! You currently have 6,331 active businesses across Spain (2,494), France (2,127), and Germany (1,710). Would you like me to help you search for specific types of businesses or locations?",
                'countries': "ListAcrossEU currently covers 3 countries with data: 🇪🇸 Spain, 🇫🇷 France, and 🇩🇪 Germany. We're expanding soon to 🇳🇱 Netherlands, 🇵🇹 Portugal, and 🇧🇪 Belgium! Which country interests you most?",
                'spain': "Spain has 2,494 active businesses in our directory! Major cities include Madrid, Barcelona, Valencia, and Seville. Would you like to explore businesses in a specific Spanish city?",
                'france': "France has 2,127 businesses listed! Key cities are Paris, Lyon, Marseille, and Toulouse. What type of French business are you looking for?",
                'germany': "Germany features 1,710 businesses in our platform! Major cities include Berlin, Munich, Hamburg, and Frankfurt. How can I help you find German businesses?",
                'language': "I can help in all 27 EU languages! 🇪🇺 Currently available: Bulgarian, Croatian, Czech, Danish, Dutch, English, Estonian, Finnish, French, German, Greek, Hungarian, Irish, Italian, Latvian, Lithuanian, Maltese, Polish, Portuguese, Romanian, Slovak, Slovenian, Spanish, Swedish, plus regional languages. Which would you prefer?"
            },
            'es': {
                'businesses': "¡Encontré tus datos de empresas! Actualmente tienes 6,331 empresas activas en España (2,494), Francia (2,127) y Alemania (1,710). ¿Te gustaría que te ayude a buscar tipos específicos de empresas o ubicaciones?",
                'countries': "ListAcrossEU actualmente cubre 3 países con datos: 🇪🇸 España, 🇫🇷 Francia y 🇩🇪 Alemania. ¡Pronto expandiremos a 🇳🇱 Países Bajos, 🇵🇹 Portugal y 🇧🇪 Bélgica! ¿Qué país te interesa más?",
                'spain': "¡España tiene 2,494 empresas activas en nuestro directorio! Las ciudades principales incluyen Madrid, Barcelona, Valencia y Sevilla. ¿Te gustaría explorar empresas en una ciudad española específica?",
                'language': "¡Puedo ayudar en los 27 idiomas de la UE! 🇪🇺 ¿Cuál prefieres?"
            },
            'fr': {
                'businesses': "J'ai trouvé vos données d'entreprises! Vous avez actuellement 6,331 entreprises actives en Espagne (2,494), France (2,127) et Allemagne (1,710). Voulez-vous que je vous aide à rechercher des types spécifiques d'entreprises ou d'emplacements?",
                'countries': "ListAcrossEU couvre actuellement 3 pays avec des données: 🇪🇸 Espagne, 🇫🇷 France et 🇩🇪 Allemagne. Nous étendons bientôt vers 🇳🇱 Pays-Bas, 🇵🇹 Portugal et 🇧🇪 Belgique! Quel pays vous intéresse le plus?",
                'france': "La France a 2,127 entreprises répertoriées! Les villes clés sont Paris, Lyon, Marseille et Toulouse. Quel type d'entreprise française recherchez-vous?",
                'language': "Je peux aider dans les 27 langues de l'UE! 🇪🇺 Laquelle préférez-vous?"
            }
        };

        const langResponses = responses[lang] || responses['en'];

        for (const [key, response] of Object.entries(langResponses)) {
            if (lowerInput.includes(key)) {
                return response;
            }
        }

        // Default response
        const defaultResponses: Record<string, string> = {
            'en': "I'm here to help you navigate ListAcrossEU! I can assist with finding businesses, country information, statistics, or language changes. Try asking about 'businesses in Spain' or 'platform statistics'!",
            'es': "¡Estoy aquí para ayudarte a navegar ListAcrossEU! Puedo asistir con encontrar empresas, información de países, estadísticas o cambios de idioma. ¡Intenta preguntar sobre 'empresas en España' o 'estadísticas de la plataforma'!",
            'fr': "Je suis là pour vous aider à naviguer ListAcrossEU! Je peux vous aider à trouver des entreprises, des informations sur les pays, des statistiques ou des changements de langue. Essayez de demander 'entreprises en Espagne' ou 'statistiques de la plateforme'!",
            'de': "Ich bin hier, um Ihnen bei der Navigation in ListAcrossEU zu helfen! Ich kann bei der Suche nach Unternehmen, Länderinformationen, Statistiken oder Sprachänderungen helfen. Versuchen Sie 'Unternehmen in Spanien' oder 'Plattform-Statistiken' zu fragen!"
        };

        return defaultResponses[lang] || defaultResponses['en'];
    };

    const getErrorMessage = (lang: string): string => {
        const errorMessages: Record<string, string> = {
            'en': "I'm sorry, I encountered an error. Please try again or ask something else!",
            'es': "Lo siento, encontré un error. ¡Por favor intenta de nuevo o pregunta algo más!",
            'fr': "Désolé, j'ai rencontré une erreur. Veuillez réessayer ou demander autre chose!",
            'de': "Entschuldigung, ich bin auf einen Fehler gestoßen. Bitte versuchen Sie es erneut oder fragen Sie etwas anderes!"
        };
        return errorMessages[lang] || errorMessages['en'];
    };

    const handleQuickAction = (action: string) => {
        setInputValue(action);
        inputRef.current?.focus();
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    if (!isOpen) {
        return (
            <div className="fixed bottom-6 right-6 z-50">
                <button
                    onClick={() => setIsOpen(true)}
                    className="bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full p-4 shadow-2xl hover:scale-110 transition-all duration-300 animate-pulse"
                    title="Chat with Listy"
                >
                    <div className="flex items-center space-x-2">
                        <span className="text-2xl">🤖</span>
                        <span className="font-bold hidden sm:block">Listy</span>
                    </div>
                </button>
            </div>
        );
    }

    return (
        <div className="fixed bottom-6 right-6 z-50">
            <div className={`bg-white rounded-2xl shadow-2xl border border-gray-200 transition-all duration-300 ${isMinimized ? 'h-16 w-80' : 'h-96 w-80 sm:w-96'
                }`}>
                {/* Header */}
                <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 rounded-t-2xl flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                        <span className="text-2xl animate-bounce">🤖</span>
                        <div>
                            <h3 className="font-bold text-lg">Listy</h3>
                            <p className="text-xs text-blue-100">EU Business Assistant</p>
                        </div>
                        <span className="text-lg">{currentLang.flag}</span>
                    </div>
                    <div className="flex space-x-2">
                        <button
                            onClick={() => setIsMinimized(!isMinimized)}
                            className="text-white hover:bg-white/20 rounded-full p-1 transition-colors"
                        >
                            <span className="text-lg">{isMinimized ? '▲' : '▼'}</span>
                        </button>
                        <button
                            onClick={() => setIsOpen(false)}
                            className="text-white hover:bg-white/20 rounded-full p-1 transition-colors"
                        >
                            ✕
                        </button>
                    </div>
                </div>

                {!isMinimized && (
                    <>
                        {/* Messages */}
                        <div className="h-64 overflow-y-auto p-4 space-y-3">
                            {messages.map((message) => (
                                <div
                                    key={message.id}
                                    className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
                                >
                                    <div className={`max-w-xs rounded-2xl p-3 ${message.isUser
                                            ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white'
                                            : 'bg-gray-100 text-gray-800'
                                        }`}>
                                        <p className="text-sm">{message.content}</p>
                                        <p className="text-xs mt-1 opacity-70">
                                            {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                        </p>
                                    </div>
                                </div>
                            ))}

                            {isLoading && (
                                <div className="flex justify-start">
                                    <div className="bg-gray-100 rounded-2xl p-3">
                                        <div className="flex space-x-2">
                                            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                                            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                                            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                                        </div>
                                    </div>
                                </div>
                            )}

                            <div ref={messagesEndRef} />
                        </div>

                        {/* Quick Actions */}
                        <div className="px-4 pb-2">
                            <div className="flex flex-wrap gap-1">
                                {(quickActions[selectedLanguage] || quickActions['en']).slice(0, 3).map((action, index) => (
                                    <button
                                        key={index}
                                        onClick={() => handleQuickAction(action)}
                                        className="text-xs bg-blue-50 text-blue-600 px-2 py-1 rounded-full hover:bg-blue-100 transition-colors"
                                    >
                                        {action}
                                    </button>
                                ))}
                            </div>
                        </div>

                        {/* Input */}
                        <div className="p-4 border-t border-gray-200">
                            <div className="flex space-x-2">
                                <input
                                    ref={inputRef}
                                    type="text"
                                    value={inputValue}
                                    onChange={(e) => setInputValue(e.target.value)}
                                    onKeyPress={handleKeyPress}
                                    placeholder={selectedLanguage === 'es' ? 'Escribe tu mensaje...' :
                                        selectedLanguage === 'fr' ? 'Tapez votre message...' :
                                            selectedLanguage === 'de' ? 'Nachricht eingeben...' :
                                                'Type your message...'}
                                    className="flex-1 border border-gray-300 rounded-full px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    disabled={isLoading}
                                />
                                <button
                                    onClick={handleSendMessage}
                                    disabled={isLoading || !inputValue.trim()}
                                    className="bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-full p-2 hover:scale-110 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    <span className="text-lg">🚀</span>
                                </button>
                            </div>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
}