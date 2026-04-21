import ollama
import subprocess
import re
import json
import os

class LLMEngine:
    def __init__(self, model_name="llama3"):
        self.model_name = model_name
        self.workspace = "workspace"
        self.system_instructions = self._load_prompt("system_prompt.txt")
        self.history = [] 
        
        if not os.path.exists(self.workspace):
            os.makedirs(self.workspace)

    def _load_prompt(self, filename):
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            return "You are a terminal assistant."
        except Exception as e:
            return f"Error loading prompt: {str(e)}"

    def execute_command(self, command):
        """จัดการรันคำสั่งพร้อมระบบจัดการ Timeout สำหรับ Server"""
        try:
            # ใช้ subprocess.Popen เพื่อให้สามารถจัดการ timeout ได้ยืดหยุ่นขึ้น
            process = subprocess.run(
                command, 
                shell=True, 
                cwd=self.workspace, 
                capture_output=True, 
                text=True,
                timeout=15  # ตั้งไว้ 15 วินาทีสำหรับคำสั่งทั่วไป
            )
            output = (process.stdout + process.stderr).strip()
            return output if output else "Command executed successfully (no output)."
        
        except subprocess.TimeoutExpired as e:
            # ถ้า Timeout (มักเกิดจากรัน Flask/Server ค้างไว้)
            # เราจะถือว่ามันทำงานอยู่ และส่ง stdout เท่าที่เก็บได้กลับไป
            partial_output = e.stdout.decode() if e.stdout else ""
            return f"Command timed out but might be running in background. Current Output: {partial_output}"
        except Exception as e:
            return f"Execution Error: {str(e)}"

    def chat(self, prompt):
        self.history.append({'role': 'user', 'content': prompt})

        try:
            messages = [{'role': 'system', 'content': self.system_instructions}] + self.history
            
            response = ollama.chat(model=self.model_name, messages=messages)
            content = response['message']['content']
            
            # บันทึกสิ่งที่ AI ตอบลง history ทันที
            self.history.append({'role': 'assistant', 'content': content})

            # ปรับ Regex ให้ดักจับ JSON ภายใน code block หรือ text ปกติได้แม่นขึ้น
            pattern = r'exec\s*(\{[^}]+\})'
            matches = re.findall(pattern, content)
            
            if matches:
                exec_results = []
                for match in matches:
                    try:
                        data = json.loads(match)
                        cmd = data.get("command")
                        if cmd:
                            # ป้องกัน AI แอบใช้ ~ หรือ path นอก workspace
                            if "~" in cmd or ".." in cmd:
                                # บังคับลบ path หลอกล่อออกเพื่อให้รันใน workspace เท่านั้น
                                cmd = cmd.replace("~/", "./").replace("../", "")

                            print(f"\n\033[91m[Running]\033[0m {cmd}")
                            out = self.execute_command(cmd)
                            
                            # FEEDBACK: ส่งผลลัพธ์กลับไปให้ AI รู้ว่ารันจริงแล้วได้อะไร
                            self.history.append({
                                'role': 'system', 
                                'content': f"Execution Result for [{cmd}]:\n{out}"
                            })
                            exec_results.append(f"\n\033[96m[Output]\033[0m\n{out}")
                    except json.JSONDecodeError:
                        continue
                
                return content + "\n" + "\n".join(exec_results)
            
            return content
        except Exception as e:
            return f"Runtime Error: {str(e)}"
