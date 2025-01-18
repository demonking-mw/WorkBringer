"""
takes in the list of importance of attributes
returns a list with identical structure, but every weight should be changed
TO GET THIS WORKING: follow the beginner guide on the gpt official website
to get the key and store it in an env file, also put it in environment var.
"""

from openai import OpenAI
import os


class GPT_Attribute:
    """
    set attribute list through gpt.
    """

    def get_gpt_out(self, input_message: list, gpt_model: str) -> str:
        """
        Gets the output from ChatGPT with a given input
        """
        print("COMMENCE GPT RETRIVAL ATTEMPT")
        client = OpenAI()
        completion = client.chat.completions.create(
            model=gpt_model, messages=input_message
        )
        print("TOKEN_USED:")
        print(completion.usage.total_tokens)
        return completion.choices[0].message

    def set_simple(self, input_message: str) -> list:
        """
        makes the dictionary that gets fed into get_gpt_out
        """
        messages = [{"role": "user", "content": input_message}]
        return messages

    def get_job_description(self):
        """
        Can potentially be modded to implement web scraping
        """
        result = ""
        if self.all_job_info == "":
            result += "JOB SUMMARY: "
            result += self.job_sum + "\n"
            result += "JOB RESPONSIBILITIES: "
            result += self.job_resp + "\n"
            result += "REQUIRED SKILL: "
            result += self.job_req + "\n"
        else:
            result = self.all_job_info

        return result

    def get_init_prompt(self) -> list:
        """
        generates the first prompt for GPT
        """
        prompt = self.opening_line + "\n"
        prompt += "traits: ["
        for item in self.att_list:
            prompt += item[0] + ", "
        prompt += "]\n"
        prompt += self.answer_style_guide + "\n"
        prompt += self.att_list[0][0] + "=(your answer)"
        prompt += self.get_job_description()
        return self.set_simple(prompt)

    def search_in_result(self, gpt_result, target) -> int:
        """
        search for target attribute in some GPT result
        returns the attribute's value
        """
        # Find the index of the target string
        index = gpt_result.find(target)
        result = 1
        # Check if the target was found and if there is a character after it
        if index != -1 and index + len(target) < len(gpt_result):
            character_after_target = gpt_result[index + len(target) + 1]
            result = int(character_after_target)
        else:
            print("ERROR")
            print(f"Target: {target} not found in GPT result")
        return result

    def fill_list(self) -> list:
        """
        edits the att_list
        """
        result = {"tech": [], "soft": [], "asset": []}
        for item in self.att_list["tech"]:
            value = self.search_in_result(self.first_response, item[0])
            result["tech"].append([item[0], value])
        for item in self.att_list["soft"]:
            value = self.search_in_result(self.first_response, item[0])
            result["soft"].append([item[0], value])
        for item in self.att_list["asset"]:
            value = self.search_in_result(self.first_response, item[0])
            result["asset"].append([item[0], value])
        return result

    def __init__(
        self,
        att_list: list[list],
        model_name: str,
        job_sum: str,
        job_resp: str,
        job_req: str,
        all_job_info: str = "",
    ) -> None:
        self.att_list = att_list
        self.job_sum = job_sum
        self.job_resp = job_resp
        self.job_req = job_req
        self.all_job_info = all_job_info
        self.opening_line = "Analyze the following job description, give each trait/skill in the list below a value between 0 to 9, inclusive. The value reflects how much the skill helps in getting the job, and how much the recruiter would value the skill. You should also consider how relevant the skill is to the job, as skills in proximity to what the recruiter desires should be awarded with some value."
        self.answer_style_guide = (
            "your response must cover each trait in the format of:"
        )
        self.first_response_dic = self.get_gpt_out(self.get_init_prompt(), model_name)
        print("GPT RESPONSE:")
        print(self.first_response_dic)
        print()
        self.first_response = self.first_response_dic.content
        self.gpt_modded_list = self.fill_list()
        self.generate_debug_file()

    def generate_debug_file(self):
        """
        generate a file with gpt informations.
        """
        result = ""
        result += "QUERY:\n"
        result += self.get_job_description() + "\n\n"
        result += "RESPONSE:\n"
        result += str(self.gpt_modded_list) + "\n\n"
        result += "FULL RESPONSE:\n"
        result += str(self.first_response_dic)
        result = result.encode("ascii", "ignore").decode("ascii")
        documents_folder = os.path.join(
            os.path.expanduser("~"), "OneDrive", "Documents", "Resumes"
        )
        os.makedirs(documents_folder, exist_ok=True)
        counter = 1
        while os.path.exists(
            os.path.join(documents_folder, f"gpt_debug_{counter}.txt")
        ):
            counter += 1
        debug_file_name = f"gpt_debug_{counter}.txt"
        file_path = os.path.join(documents_folder, debug_file_name)
        print("DEBUG: ATTRIBUTE AT", file_path)
        with open(file_path, "w") as f:
            f.write(result)
