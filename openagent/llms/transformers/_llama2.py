from .._transformers import Transformers
import transformers

class LLaMA2(Transformers):
    """ 
    A HuggingFace transformers version of the LLaMA2 language model with compiler support.
    """

    llm_name: str = "llama2"

    def _model_and_tokenizer(self, model, tokenizer, **kwargs):
        # load the LLaMA2 specific tokenizer and model
        if isinstance(model, str):
            if tokenizer is None:
                tokenizer = transformers.LlamaTokenizer.from_pretrained(
                    model, 
                    add_special_tokens={"pad_token":"<pad>"}, 
                    **kwargs
                )
                tokenizer.model_max_length = transformers.LlamaConfig().max_position_embeddings
            model = transformers.LlamaForCausalLM.from_pretrained(model, **kwargs)
            model.config.pad_token_id = tokenizer.pad_token_id
            
        return super()._model_and_tokenizer(model, tokenizer, **kwargs)
