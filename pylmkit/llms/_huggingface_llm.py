from pylmkit.utils.data_utils import stream_print


class LocalLLMModel(object):
    def __init__(self, model_path, language="en", tokenizer_kwargs=None, model_kwargs=None):
        import torch, logging
        import transformers
        self.history = []
        if tokenizer_kwargs is None:
            tokenizer_kwargs = {}
        if model_kwargs is None:
            model_kwargs = {}
        if language in ['zh']:
            try:
                import modelscope
            except:
                raise Exception("Please install `pip install modelscope`")
            self.tokenizer = modelscope.AutoTokenizer.from_pretrained(model_path,
                                                                      trust_remote_code=True,
                                                                      **tokenizer_kwargs
                                                                      )
            self.model = modelscope.AutoModelForCausalLM.from_pretrained(model_path,
                                                                         device_map="auto",
                                                                         offload_folder=model_path,
                                                                         trust_remote_code=True,
                                                                         **model_kwargs
                                                                         )
        else:
            self.tokenizer = transformers.AutoTokenizer.from_pretrained(model_path,
                                                                        trust_remote_code=True,
                                                                        **tokenizer_kwargs
                                                                        )
            self.model = transformers.AutoModelForCausalLM.from_pretrained(model_path,
                                                                           trust_remote_code=True,
                                                                           **model_kwargs
                                                                           )

        if torch.cuda.is_available():  # GPU
            # print("CUDA")
            self.model = self.model.half().cuda()
        else:  # CPU
            # print("CPU")
            self.model = self.model.float()
        self.model = self.model.eval()

    def invoke(self, query, history=None, **kwargs):
        # system=""  system相当于一个预设角色和引导作用
        response, self.history = self.model.chat(self.tokenizer, query, history=history, **kwargs)
        return response

    def stream(self, query, history=None, buffer_size=3, **kwargs):
        response, self.history = self.model.chat(self.tokenizer, query, history=history, **kwargs)
        return stream_print(response, buffer_size=buffer_size)



