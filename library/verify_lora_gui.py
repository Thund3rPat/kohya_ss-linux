import gradio as gr
from easygui import msgbox
import subprocess
import os
from .common_gui import (
    get_saveasfilename_path,
    get_any_file_path,
    get_file_path,
)

folder_symbol = '\U0001f4c2'  # 📂
refresh_symbol = '\U0001f504'  # 🔄
save_style_symbol = '\U0001f4be'  # 💾
document_symbol = '\U0001F4C4'   # 📄


def verify_lora(
    lora_model,
):
    # verify for caption_text_input
    if lora_model == '':
        msgbox('Invalid model A file')
        return

    # verify if source model exist
    if not os.path.isfile(lora_model):
        msgbox('The provided model A is not a file')
        return

    run_cmd = f'python3 "networks/check_lora_weights.py"'
    run_cmd += f' {lora_model}'

    print(run_cmd)

    # Run the command
    subprocess.run(run_cmd, shell=True)
    process = subprocess.Popen(run_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    return (output.decode(), error.decode())


###
# Gradio UI
###


def gradio_verify_lora_tab():
    with gr.Tab('Verify LoRA'):
        gr.Markdown(
            'This utility can verify a LoRA network to make sure it is properly trained.'
        )

        lora_ext = gr.Textbox(value='*.pt *.safetensors', visible=False)
        lora_ext_name = gr.Textbox(value='LoRA model types', visible=False)

        with gr.Row():
            lora_model = gr.Textbox(
                label='LoRA model',
                placeholder='Path to the LoRA model to verify',
                interactive=True,
            )
            button_lora_model_file = gr.Button(
                folder_symbol, elem_id='open_folder_small'
            )
            button_lora_model_file.click(
                get_file_path,
                inputs=[lora_model, lora_ext, lora_ext_name],
                outputs=lora_model,
            )
            verify_button = gr.Button('Verify', variant='primary')

        lora_model_verif_output = gr.Textbox(
            label='Output',
            placeholder='Verification output',
            interactive=False,
            lines=1,
            max_lines=10,
        )

        lora_model_verif_error = gr.Textbox(
            label='Error',
            placeholder='Verification error',
            interactive=False,
            lines=1,
            max_lines=10,
        )

        verify_button.click(
            verify_lora,
            inputs=[
                lora_model,
            ],
            outputs=[lora_model_verif_output, lora_model_verif_error],
        )
