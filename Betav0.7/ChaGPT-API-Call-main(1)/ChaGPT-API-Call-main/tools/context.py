from tools.utils import del_context
import re
import json
from tools import draw
class ContextHandler(object):
   
    def __init__(self,max_context=3200,context_del_config=None):
        super().__init__()
        self.context = []
        self.role_lengths = []
        self.max_context = max_context

        # the config of del context
        self.context_del_config = context_del_config

    def append_cur_to_context(self,data,complete__length,tag=0):

        if tag == 0:
            role = "user"
        elif tag == 1:
            role = "assistant"
        else:
            role = "system"

        role_data = {"role": role, "content": data}
        self.context.append(role_data)
        # ʹ��'a'ģʽ���ļ�������ļ������ڣ�����������
        # ������������ַ���
        # ʹ��������ʽ�ҵ�[]�������
        Scenedata = None
        match = re.search(r'\[(.*?)\]',role_data["content"]) 
        file_path =r"../output/sessionlog.txt"  
        if match and role=="assistant":#ȥ��roleΪ��ʱ,д������
            # ����ҵ���ƥ�䣬�������Scenedata������
              Scenedata = match.group(1)
        if Scenedata is not None and role=="assistant":
            draw.set_last_position(file_path)
            with open(file_path, 'a+', encoding='utf8') as file:
                file.write(json.dumps(Scenedata))
            draw.DrawPainting()
        self.role_lengths.append(complete__length)

    def cut_context(self,cur_total_length,tokenizer):
        if self.context_del_config:
            del_context(self.context, self.role_lengths, cur_total_length, self.max_context, tokenizer=tokenizer,
                        distance_weights=self.context_del_config.distance_weights,
                        length_weights=self.context_del_config.length_weights,
                        role_weights=self.context_del_config.role_weights,
                        sys_role_ratio=self.context_del_config.sys_role_ratio,
                        del_ratio=self.context_del_config.del_ratio,
                        max_keep_turns=self.context_del_config.max_keep_turns,
                        )
        # use the default pram
        else:
            del_context(self.context,self.role_lengths,cur_total_length,self.max_context,tokenizer=tokenizer)
    def clear(self):
        self.context.clear()