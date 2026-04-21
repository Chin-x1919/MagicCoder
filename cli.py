from core.engine import LLMEngine
import sys

def main():
    model = sys.argv[1] if len(sys.argv) > 1 else "qwen2.5-coder:7b"
    engine = LLMEngine(model_name=model)
    
    print(f"\033[94m--- Ollama Autonomous Agent | Model: {model} ---\033[0m")
    print("Type your objective, and the agent will run until 'COMPLETE!'.")
    
    while True:
        try:
            user_input = input("\n\033[92mUser Goal > \033[0m")
            if not user_input.strip(): continue
            if user_input.lower() in ['exit', 'quit']: break
            
            current_prompt = user_input
            
            # --- START AUTONOMOUS LOOP ---
            while True:
                response = engine.chat(current_prompt)
                print(f"\033[93mAssistant:\033[0m {response}")
                
                # เงื่อนไขหยุด: ถ้าไม่มีการสั่ง exec แล้ว หรือ AI บอกว่างานจบแล้ว
                if "exec{" not in response or "COMPLETE!" in response.upper():
                    print("\n\033[94m[Objective Reached or Paused]\033[0m")
                    break
                
                # ถ้ายังมี exec อยู่ ให้ส่งสถานะล่าสุดกลับไปเป็น Prompt อัตโนมัติ
                # เราใช้ string ว่างหรือข้อความกระตุ้นสั้นๆ เพื่อให้มันดู History แล้วทำงานต่อ
                current_prompt = "Continue with the next step based on the previous output."
            # --- END AUTONOMOUS LOOP ---
            
        except KeyboardInterrupt:
            print("\nStopped by user.")
            break

if __name__ == "__main__":
    main()
