pub mod commands;

use crate::agent::{api::OpenAIClient, process_session};
use crate::core::session::{FinishReason, Message, SessionData};
use crate::core::tool::ToolRegistry;
use anyhow::Result;
use std::io::{self, Write};

pub async fn run_interactive(
    tool_registry: &ToolRegistry,
    client: &OpenAIClient,
    session_data: &SessionData,
) -> Result<()> {
    println!("=== YAA 智能体命令行交互模式 ===");
    println!("输入 '/exit' 退出");

    let mut session = session_data.clone();

    loop {
        // 输出提示符
        print!("> ");
        io::stdout().flush()?;

        // 读取用户输入
        let mut input = String::new();
        io::stdin().read_line(&mut input)?;
        let input = input.trim();

        if input.eq_ignore_ascii_case("/exit") {
            break;
        }

        // 添加用户消息
        session.messages.push(Message {
            role: crate::core::session::Role::User,
            content: input.to_string(),
        });

        // 处理会话
        let response = process_session(session.clone(), tool_registry, client).await?;

        // 输出响应消息
        for msg in &response.messages {
            println!("【{:?}】\n{}", msg.role, msg.content);
            session.add_message(msg.role.clone(), msg.content.clone());
        }

        // 检查会话是否结束
        if matches!(
            response.finish_reason,
            FinishReason::Completed | FinishReason::Failed
        ) {
            break;
        }
    }

    Ok(())
}
