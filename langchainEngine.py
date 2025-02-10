from typing import Any, Dict, Iterator, List, Optional

from langchain_core.callbacks import (
    CallbackManagerForLLMRun,
)
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, AIMessageChunk, BaseMessage, HumanMessage
from langchain_core.messages.ai import UsageMetadata
from langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult
from pydantic import Field

import sys

sys.path.append("./")

from internvl_node import chat_with_internvl


class InternlVL(BaseChatModel):
    """A custom chat model that echoes the first `parrot_buffer_length` characters
    of the input.

    When contributing an implementation to LangChain, carefully document
    the model including the initialization parameters, include
    an example of how to initialize the model and include any relevant
    links to the underlying models documentation or API.

    Example:

        .. code-block:: python

            model = ChatParrotLink(parrot_buffer_length=2, model="bird-brain-001")
            result = model.invoke([HumanMessage(content="hello")])
            result = model.batch([[HumanMessage(content="hello")],
                                 [HumanMessage(content="world")]])
    """

    model_name: str = Field(alias="model")
    """The name of the model"""
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    timeout: Optional[int] = None
    stop: Optional[List[str]] = None
    max_retries: int = 2

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Override the _generate method to implement the chat model logic.

        This can be a call to an API, a call to a local model, or any other
        implementation that generates a response to the input prompt.

        Args:
            messages: the prompt composed of a list of messages.
            stop: a list of strings on which the model should stop generating.
                  If generation stops due to a stop token, the stop token itself
                  SHOULD BE INCLUDED as part of the output. This is not enforced
                  across models right now, but it's a good practice to follow since
                  it makes it much easier to parse the output of the model
                  downstream and understand why generation stopped.
            run_manager: A run manager with callbacks for the LLM.
        """
        # Replace this with actual logic to generate a response from a list
        # of messages.
        last_message = messages[-1]
        print("InternVL: ", messages)
        result = chat_with_internvl(messages)

        message = AIMessage(
            content=result.choices[0].message.content,
            additional_kwargs={},  # Used to add additional payload to the message
            response_metadata={  # Use for response metadata
                "time_in_seconds": 3,
            },
            usage_metadata={
                "input_tokens": 50,
                "output_tokens": 75,
                "total_tokens": 125,
            },
        )
        ##

        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])

    @property
    def _llm_type(self) -> str:
        """Get the type of language model used by this chat model."""
        return "InternVL"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return a dictionary of identifying parameters.

        This information is used by the LangChain callback system, which
        is used for tracing purposes make it possible to monitor LLMs.
        """
        return {
            # The model name allows users to specify custom token counting
            # rules in LLM monitoring applications (e.g., in LangSmith users
            # can provide per token pricing for their model and monitor
            # costs for the given LLM.)
            "model_name": self.model_name,
        }


def run_interVL_chain(image: bytes, description: str, history: List[dict]):
    history = convert_history(history)
    message = [
        HumanMessage(
            content=[
                {"type": "text", "content": f"{description}"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"{image}"},
                },
            ]
        )
    ]
    if len(history) != 0:
        message = history + message
    result = model.invoke(message)
    return result


def convert_history(history: List[dict]) -> list:
    message = []
    for i in history:
        message.append(
            HumanMessage(
                content=[
                    {"type": "text", "content": f"{i['HumanMessage']}"},
                    {"type": "image_url", "image_url": {"url": f"{i['image_url']}"}},
                ]
            )
        )
        message.append(
            AIMessage(
                content=[
                    {"type": "text", "content": f"{i['AIMessage']}"},
                ]
            )
        )
    return message


model = InternlVL(model="InternVL")

if __name__ == "__main__":
    # doc: https://python.langchain.com/docs/how_to/multimodal_inputs/
    from langchain_core.messages import HumanMessage
    import base64

    with open("media\IMG1808_9118.JPG", "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    result = model.invoke(
        [
            HumanMessage(
                content=[
                    {"type": "text", "content": "what you see in the picture?"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
                    },
                ]
            )
        ]
    )
    print(result)
