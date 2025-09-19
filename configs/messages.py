class ErrorMessages:
    INVALID_INPUT = "The input provided is invalid."
    NOT_FOUND = "The requested resource was not found."
    SERVER_ERROR = "An internal server error has occurred."
    UNAUTHORIZED = "You do not have permission to access this resource."
    TIMEOUT = "The request has timed out. Please try again later."
    API_KEY_MISSING = "I can't start because my API key is missing or invalid. Please check the dot env file."
    API_KEY_ISSUE = "I couldn't start properly. There might be an issue with my API key."
    STARTUP_ERROR = "Something went wrong during startup. Please check the logs."
    NETWORK_CONNECTION_ERROR = "I'm having trouble connecting to the internet. Please check your connection."
    AUDIO_NOT_UNDERSTOOD = "I didn't catch that. Please try again."
    TOOL_UNKNOWN = "I don't know how to use the tool {tool_name}."
    TOOL_EXECUTION_ERROR = "I encountered an error while using {tool_name}. {error}"
    ROUTER_ERROR = "I'm having trouble connecting to my brain right now. There might be an issue with my API key or connection."
    NETWORK_OFFLINE = "❌ No internet connection detected."
    SPEECH_NOT_UNDERSTOOD = "❓ Sorry, I did not understand that."
    NETWORK_RETRY = "❗ Network error. Retrying in {delay} sec..."

class InfoMessages:
    WELCOME = "Welcome to the application! How can I assist you today?"
    GOODBYE = "Thank you for using the application. Have a great day!"
    PROCESSING = "Your request is being processed. Please wait..."
    SUCCESS = "The operation was completed successfully."
    RETRY = "Please try again."
    ASSISTANT_STARTING = "{assistant_name} is just a moment..."
    ASSISTANT_READY = "now online and ready to assist you. Just say {assistant_name} to activate me."
    LISTENING = "Yes, I'm listening"
    WAITING_FOR_NETWORK = "Oh no! The Wi-Fi ghost stole our internet. Let's wait a bit..."
    GOODBYE_MESSAGE = "Goodbye! See you later."
    MICROPHONE_LISTENING = "👂 Eva listening..."
    USER_SAID = "🗣️ You said: {text}"
    HEARD_WAKE_WORD = "🗣️ Heard: {text}"
    
class SuccessMessages:
    DATA_SAVED = "Your data has been saved successfully."
    EMAIL_SENT = "The email has been sent successfully."
    ACCOUNT_CREATED = "Your account has been created successfully."
    PASSWORD_CHANGED = "Your password has been changed successfully."
    LOGGED_IN = "You have logged in successfully."
    APP_OPENED = "{app_name} opened successfully."
    VOLUME_SET = "Volume set to {level}%."
    FOLDER_CREATED = "Folder '{folder_name}' created successfully at {path}."
    COMPUTER_SHUTDOWN = "Computer will shutdown in {delay} seconds."
    COMPUTER_RESTART = "Computer will restart in {delay} seconds."
    COMPUTER_SLEEP = "Computer is going to sleep."
    COMPUTER_LOCKED = "Computer has been locked."
    SHUTDOWN_CANCELLED = "Shutdown has been cancelled."

class DefaultResponses:
    FALLBACK_RESPONSE = "I'm not sure how to respond to that."
    API_KEY_CHECK_ERROR = "There seems to be an issue with my API key. Please check the OPENROUTER_API_KEY in your .env file and make sure it's valid."



