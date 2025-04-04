import importlib
import platform

from yaa.PromptGen.BasePromptGenerater import BasePromptGenerater
import yaa.Tools as tools
from yaa.Config.Config import Config
from yaa.Stream.StreamTools import StreamTools as st
from yaa.Error.ErrorHandler import ErrorHandler as eh

class PromptGenerater(BasePromptGenerater):
    def _init(self, session_data):
        self.character = session_data.get('character', '您是 `yaa`，一个智能体。')
        self.start_time = session_data['start_time']
        self.lang = session_data['config']['yaa'].get('language', Config.YAA_CONFIG['language'])

    def PromptGenerate(self, session_data, stream_func=None):
        '''生成提示词'''
        try:
            stream_tools = st(session_data)
            self._init(session_data)
            if len(session_data['messages']) <= 1 and session_data['messages'][-1]['role'] == 'user':
                role = 'system'
                content = ''
                status = '进行中'

                # 添加格式化的用户任务
                content += self._gen_xml("用户任务", session_data['messages'][-1]['content'])
                stream_tools.update_stream(
                    content=self._gen_xml("用户任务", session_data['messages'][-1]['content']),
                    session_data=session_data,
                    role=role,
                    status=status,
                    stream_func=stream_func
                )

                # 添加角色信息
                content += self._add_character_info()
                stream_tools.update_stream(
                    content=self._add_character_info(),
                    session_data=session_data,
                    role=role,
                    status=status,
                    stream_func=stream_func
                )

                # 添加工具信息
                content += self._add_tools_info()
                stream_tools.update_stream(
                    content=self._add_tools_info(),
                    session_data=session_data,
                    role=role,
                    status=status,
                    stream_func=stream_func
                )

                # 添加规则信息
                content += self._add_rules_info()
                stream_tools.update_stream(
                    content=self._add_rules_info(),
                    session_data=session_data,
                    role=role,
                    status=status,
                    stream_func=stream_func
                )

                # 添加目标信息
                content += self._add_objectives_info()
                stream_tools.update_stream(
                    content=self._add_objectives_info(),
                    session_data=session_data,
                    role=role,
                    status=status,
                    stream_func=stream_func
                )

                # 添加环境信息
                content += self._add_env_info()
                stream_tools.update_stream(
                    content=self._add_env_info(),
                    session_data=session_data,
                    role=role,
                    status=status,
                    stream_func=stream_func
                )

                # 添加自定义指示
                content += self._add_custom_info()
                stream_tools.update_stream(
                    content=self._add_custom_info(),
                    session_data=session_data,
                    role=role,
                    status=status,
                    stream_func=stream_func
                )
                
                message = {
                    "role": role,
                    "content": content
                }

                session_data['messages'].append(message)
            
            return session_data
        except Exception as e:
            return eh.return_error_msg(session_data=session_data, error=e, task_name='提示词生成', stream_func=stream_func)

    def _gen_xml(cls, name, inline):
        return f'<{name}>\n{inline}\n</{name}>\n'

    def _add_user_task(self, user_task):
        '''添加用户任务
        输入：
            user_task: 用户输入的任务
        输出：
            user_task: 格式化的用户任务
        '''
        return self._gen_xml("用户任务", user_task)

    def _add_character_info(self):
        '''添加角色信息
        输入：
            session_data: 会话数据
        输出：
            character_info: 角色信息
        '''
        return self._gen_xml("角色", self.character)

    def _gen_title_content(cls, title, content):
        return f'## {title}\n\n{content}\n\n'

    def _add_custom_info(self):
        '''添加自定义指示
        输入：
            session_data: 会话数据
        输出：
            custom_info: 自定义指示
        '''
        custom_info = '# 用户自定义指示\n\n以下附加指示由用户提供，应尽量遵守，但不得违反工具调用指南。\n\n'
        # 用户语言偏好
        custom_info += self._gen_title_content(
            "语言偏好",
            '您应始终用' + self.lang + '语言回答和思考，除非接下来用户给出不同的指示。'
        )

        return self._gen_xml("自定义指示", custom_info)

    def _add_env_info(self):
        '''添加环境信息
        输入：
            session_data: 会话数据
        输出：
            env_info: 环境信息
        '''
        # 时间
        env_info = self._gen_title_content("时间", self.start_time)
        # 系统信息
        env_info += self._gen_title_content("系统信息", f"{platform.platform()} {platform.architecture()}")

        return self._gen_xml("环境信息", env_info)

    def _add_tools_info(self):
        '''添加如何使调用工具的指示
        输出：
            info: 工具使用说明
        '''
        tools_info = "# 工具的调用\n\n您有能力调用一套需用户批准的工具。您可在每一条消息中调用一个工具，并在工具角色回复里收到工具的使执行结果。您应逐步调用工具来完成特指定任务，每此工具的调用都基于前一个次工具调用的结果。\n\n## 工具调用格式\n\n工具的调用采用形似 XML 风格的标签。工具名称被包含在开、闭标签之间，每个参数也类似地被包含在其自己的标签集中。结构如下：\n\n<工具名称>\n<第一个参数的名称>第一个值</第一个参数的名称>\n<第二个参数的名称>第二个值</第二个参数的名称>\n……\n</工具名称>\n\n举个例子：\n\n<完成会话>\n<理由>（对任务完成的总结）</理由>\n</完成会话>\n\n请始终遵循此格式调用工具以确保其被正确解析和执行。\n接下来为可用工具信息。\n\n"
        # 格式化所有的工具信息
        for tool_name in tools.__all__:
            tool = importlib.import_module('yaa.Tools.' + tool_name).Tool
            tool_name = tool.ToolInfo['name']
            tool_description = tool.ToolInfo['description']

            # 生成工具基本信息
            tool_info = self._gen_title_content(tool_name, tool_description)

            # 格式化参数部分
            if 'parameters' in tool.ToolInfo:
                tool_info += "### 参数\n\n"
                for param in tool.ToolInfo['parameters']['properties']:
                    required = "(必填)" if param['name'] in tool.ToolInfo['parameters']['required'] else "(可选)"
                    tool_info += f"- {param['name']}{required}，{param['type']}：{param['description']}\n"
                tool_info += "\n"

            # 格式化反馈部分
            # if 'feedback' in tool.ToolInfo:
            #     tool_info += "### 反馈\n\n"
            #     for feedback in tool.ToolInfo['feedback']['properties']:
            #         required = "(必填)" if feedback['name'] in tool.ToolInfo['feedback']['required'] else "(可选)"
            #         tool_info += f"- {feedback['name']}{required}，{feedback['type']}：{feedback['description']}\n"
            #     tool_info += "\n"

            # 添加调用方法示例
            tool_info += "### 调用方法\n\n"
            tool_info += f"<{tool.ToolInfo['name']}>\n"
            if 'parameters' in tool.ToolInfo:
                for param in tool.ToolInfo['parameters']['properties']:
                    tool_info += f"<{param['name']}>（{param['description']}）</{param['name']}>\n"
            tool_info += f"</{tool.ToolInfo['name']}>\n\n"
            
            tools_info += tool_info

        info = self._gen_xml("工具调用指南", tools_info)

        info += '<工具调用规则>\n'
        info += '0. 实事求是。宁可多收集信息也不要假设不确定的事物成立。\n'
        info += '1. 在<思考>标签中，评估已知的信息和继续完成任务所需的信息。\n'
        info += '2. 选择该任务最适合的工具，并评估是否需要更多信息以继续，以及哪些可用的工具最有效地收集这些信息。例如，调用“列出文件”工具比用“终端调用”工具运行`ls`命令更有效。最好考虑每个可用的工具，并使调用最适合当前任务步骤的工具。\n'
        info += '3. 如果需要完成多个操作，请在每一个消息调用一个工具，迭代完成任务，每个工具的使调用都要根据前一个工具的调用结果进行，不要假设任何工具调用的后果。每一步都必须根据前一步的结果进行。\n'
        info += '4. 用每个工具指定的 XML 格式来调用工具。\n'
        info += '5. 每次调用工具后，工具角色将对该工具的执行结果进行回应。这些结果将为您提供继续完成任务或做出进一步决策所需的信息。此回应可能包括：\n'
        info += '   - 工具是否执行成功，和未成功的原因。\n'
        info += '   - 响应命令行实时输出，您可能需要思考或采取行动。\n'
        info += '   - 与工具调用相关的任何其他相关反馈或信息。\n'
        info += '6. 每次调用工具后，请务必等待用户确认后再继续。在未明确确认工具角色结果的情况下，切勿假设工具执行成功。\n\n'
        info += '逐步地继续完成任务至关重要，在每次调用工具后等待工具角色的消息，然后再继续执行任务。由此您可：\n\n'
        info += '1. 确认每个步骤成功后再继续。\n'
        info += '2. 立即解决出现的任何问题或错误。\n'
        info += '3. 根据新信息或意外结果调整您的方案。\n'
        info += '4. 确保每次行动都正确地建立在之前的行动上。\n\n'
        info += '请等待并仔细考虑工具角色和用户在每次调用工具后的反应，并缜密从容地应对，做出明智的决定。此迭代过程有助于确保工作整体的成功和行动准确性。\n'
        info += '</工具调用规则>\n'

        return info

    def _add_rules_info(cls):
        '''添加规则信息
        输出：
            rules_info: 规则信息
        '''
        rules_info = '<规则>\n'
        rules_info += '- 创建新项目（例如应用程序、网站或任何软件项目）时，请将所有新文件组织到专用项目目录中，除非用户另有指定。请有逻辑地构建项目，并遵循所创建的特定项目类型的最佳实现方式。除非另有说明，否则新项目应该无需额外设置即可轻松运行，例如，大多数项目都可以用 HTML、CSS 和 JavaScript 构建——您可以在浏览器中打开它们。\n'
        rules_info += '- 在确定要包含的适当结构和文件时，请务必考虑项目的类型（例如 Python、JavaScript、Web 应用程序）。还要考虑哪些文件可能与完成任务最相关，例如，查看项目的自述文件助于您了解项目的依赖关系，您可以将这些依赖关系合并到您编写的代码中。\n'
        rules_info += '- 对代码进行更改时，请始终优先考虑采用代码的上下文。确保您的更改与现有代码库兼容，并且它们遵循项目的编码标准和最佳实现方式。\n'
        rules_info += '- 不要要求提供不必要的信息。调用提供的工具可以高效且有效地完成用户的请求。完成任务后，必须调用“完成会话”工具向用户显示结果。用户可以提供反馈，您可以利用这些反馈进行改进并重试。\n'
        rules_info += '- 您只能调用”提问“工具向用户提问。仅当您需要其他详细信息来完成任务时调用此工具，并确保用清晰简洁的问题，这将帮助您继续完成任务。当您提出问题时，请根据您的问题为用户提供二到四个建议的答案，这样他们就不需要做太多的输入。建议应该是具体的、可行的，并且与已完成的任务直接相关。它们应按优先级或逻辑顺序排序。不过，如果您可以调用其它可用工具以避免向用户提问，请调用那个工具。例如，如果用户提到的文件可能位于外部目录（如桌面文件夹）中，则应调用“列出文件“工具列出桌面文件夹中的文件，并检查提到的文件是否存在，而不是要求用户提供文件路径。\n'
        rules_info += '- MCP 操作一次应只调用一个，与其他工具的调用方式类似。请等待确认成功，然后再继续执行其他作。\n'
        rules_info += '- 每次调用工具后，请务必等待工具角色的响应，以确认工具执行是否成功。\n'
        rules_info += '</规则>\n'
        return rules_info

    def _add_objectives_info(cls):
        '''添加目标信息
        输出：
            objectives_info: 目标信息
        '''
        objectives_info = '<目标>\n\n'
        objectives_info += '请一步一步地完成给定的任务，将其分解为清晰的步骤，实事求是、有条不紊地完成它们。\n\n'
        objectives_info += '1. 分析用户的任务并设定明确、可实现的目标来完成它。按逻辑顺序确定这些目标的优先级。\n'
        objectives_info += '2. 按顺序完成这些目标，根据需要，一次调用一个可用的工具。每个目标都要对应解决问题过程中的一个步骤。您会被告知已完成的工作以及剩余的工作。\n'
        objectives_info += '3. 记住，您有广泛的能力，可以调用各种工具，这些工具可以根据需要以巧妙的方式实现各个目标。调用工具前，请在<思考></思考>中进行分析。首先，分析“环境信息”。然后，考虑提供的哪些工具是完成用户任务的最相关工具。接下来，浏览相关工具的每个必需参数，并确定用户是否直接提供或提供了足够的信息来推断值。在决定是否可以推断参数时，请仔细考虑所有上下文，以查看它是否支持特定值。如果所有必需的参数都存在或可以合理推断，请关闭”思考“标签并继续工具调用用。但是，如果缺少必需参数的某个值，请不要调用该工具（包括调用缺失参数的相关标签），而是调用“提问”工具要求用户提供缺失的参数。如果未提供，请勿询问有关可选参数的更多信息。\n'
        objectives_info += '4. 完成用户的任务后，您必须使调用”完成会话“工具向用户显示任务的结果。\n'
        objectives_info += '5. 用户可能会提供反馈，您可以利用这些反馈进行改进并重试。但不要进行毫无意义的来回对话，即不要以问题或提供进一步帮助来结束您的回答。\n'
        objectives_info += '</目标>\n'
        return objectives_info