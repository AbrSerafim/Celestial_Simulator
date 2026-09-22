# Celestial Simulator

<div align="center">

<img src="docs/Simulador_Celeste.jpg" width="80%" >

*Celestial Simulator Interface Ideation*

----- The project runs on python 3.9.x -----

</div>

## Instalation

### 1. Clone the repository

```bash
git clone https://github.com/AbrSerafim/Celestial_Simulator
```

### 2. Setup
#### If using powershell first allow it to run scripts with

```bash
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```
#### Then run 

```bash
.\setup.ps1
```
#### The script will automatically download python 3.9.13, create a venv and install all requirements into it (Requires Microsoft App Installer: https://apps.microsoft.com/detail/9nblggh4nns1?hl=pt-BR&gl=BR)

#### Else setup python 3.9 manually then run
```bash
pip install -r requirements.txt
```