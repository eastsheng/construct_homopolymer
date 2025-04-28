import gradio as gr
import time
from rdkit import Chem
from rdkit.Chem.rdMolDescriptors import CalcMolFormula
from rdkit.Chem import Draw
from psmiles import PolymerSmiles as PS
from PIL import Image
import random
import re

def modify_smiles(smiles):
    pattern1 = r'\[\*\]'
    pattern2 = r'\(\[\*\]\)'
    smiles_m = re.sub(pattern2, '', smiles)
    smiles_m = re.sub(pattern1, '', smiles_m)
    return smiles_m


def buildpolymer(smiles,number):
    time.sleep(0.1)
    ps = PS(smiles).canonicalize
    random.seed(10)
    chain_smi = ps.random_copolymer(ps, units=int(number), ratio=0.7)

    smiles = modify_smiles(str(smiles))
    
    monomer_mol = Chem.MolFromSmiles(smiles)
    chain_smi = modify_smiles(str(chain_smi))

    chain_mol = Chem.MolFromSmiles(chain_smi)

    monomer_img = Draw.MolToImage(monomer_mol)#.save(monomer_img)
    chain_img = Draw.MolToImage(chain_mol)#.save(chain_img)

    # chain_smi = Chem.MolToSmiles(chain_mol,isomericSmiles=False)
    chain_for = CalcMolFormula(chain_mol)
    monomer_for = CalcMolFormula(monomer_mol)

    return monomer_img, chain_img, chain_smi, monomer_for, chain_for

with gr.Blocks(title="Construct Homopolymer") as demo:
    gr.Markdown(
    """
    <center>
    <br>
    <h1>🙂Construct Homopolymer-v1.0.0🙂</h1>
    Function is experimental.
    Please check results carefully.
    <br>
    </center>
    """)
    # gr.DuplicateButton(size="sm")
    with gr.Column():
        with gr.Row(equal_height=True):
            with gr.Column():
                with gr.Row():
                    # smiles = gr.Textbox(value="[*]CC([*])N1CCCC1=O",placeholder="[*]CC([*])N1CCCC1=O",lines=1,label="SMILES of Monomer")
                    smiles = gr.Textbox(lines=1,label="SMILES of Monomer")
                    # number = gr.Textbox(value=10,placeholder="10",label="Number of Monomers")
                    number = gr.Textbox(label="Number of Monomers")
                with gr.Column():
                    monomer_img = gr.Image(height=300,interactive=False)
                    monomer_for = gr.Textbox(label="Formula of Monomer",interactive=False)
            with gr.Row():
                with gr.Column():
                    polymer_img = gr.Image(height=300,interactive=False)
                    polymer_smi = gr.Textbox(label="SMILES of Polymer",interactive=True)
                    polymer_for = gr.Textbox(label="Formula of Polymer",interactive=False)

        monomer_inputs  = [smiles,number]
        polymer_outputs = [monomer_img, polymer_img, polymer_smi, monomer_for, polymer_for]

        with gr.Row(equal_height=True):
            run_btn   = gr.Button("Run")
            clear_btn = gr.ClearButton(polymer_outputs)
    run_btn.click(fn=buildpolymer, inputs=monomer_inputs, outputs=polymer_outputs)

    gr.Markdown("## Examples")
    gr.Examples([["[*]CC([*])N1CCCC1=O","10"]],fn=buildpolymer, inputs=monomer_inputs, label="PVP")

if __name__ == "__main__":
    demo.launch(favicon_path="./imgs/smile.png")