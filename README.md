# PIR – ML Model Training

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/PIR-IDS/wallet-model">
    <img src="https://avatars.githubusercontent.com/u/99486891" alt="Logo" width="130">
  </a>

  <p align="center">
    IDS: Code for the Machine Learning Model Training for the Wallet use case
    <br />
    <a href="https://github.com/PIR-IDS/wallet-model/releases"><strong>See Releases »</strong></a>
    <br />
    <br />
    <a href="https://github.com/PIR-IDS/research-paper">Research Paper</a>
    ·
    <a href="https://github.com/PIR-IDS/wallet-model/actions/workflows/test.yml">Test Results</a>
    ·
    <a href="https://github.com/PIR-IDS/.github/blob/main/profile/README.md#usage">See Global Usage</a>
  </p>
  
<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#execution">Execution</a></li>
      </ul>
    <li><a href="#tree-structure">Tree Structure</a></li>
    <li><a href="#credits">Credits</a></li>
    <li><a href="#contact">Contact</a></li>

  </ol>
</details>

***

<!-- ABOUT THE PROJECT -->
## About The Project

This code will be used in order to train the wallet model for our IDS.

To do that, it take as an input raw accelerometer data classified in two categories : "wallet" and "negative". The current input (inside the "train" folder) is the one used to generate the model of the "wallet-card" repository. These raw data also contains the gyroscope data, but these are ignored by the code. You can generate such raws input by running the "wallet-data-collector" and "ble-reader" repositories.

The train model is a CNN based only on the accelerometer data, we tried to add the gyroscope data but the benefits weren't significant. Also, we tried several sampling rates and input length and it turns out that the most efficient parameters were 96 samples at a rate of 25Hz (~4 seconds of recording).

This code is able to provide a model with an accuracy of 95% with a relatively small training set (less than 20 minutes of recording)

### Built With
* [Python](https://www.python.org/)
* [Tensorflow](https://www.tensorflow.org/)

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* Install the latest version of pyenv (https://github.com/pyenv/pyenv-installer [ UNIX ], https://pyenv-win.github.io/pyenv-win/ [ WINDOWS ]) or update it with the following command:
  ```sh
  pyenv update
  ```
* Install the latest version of pipenv (https://pipenv.pypa.io/) or update it with the following command:
  ```sh
  pip install pipenv --upgrade
  ```
  
### Installation

1. Clone the project
   ```sh
   git clone https://github.com/PIR-IDS/wallet-model.git
   ```
2. Install the dependencies by typing the following command while being in the project root:
   ```sh
   pipenv install --dev
   ```
> :warning: **If you are using pyenv-win (WINDOWS)** : If you do not have the version of Python used in the project, it is possible that pipenv does not detect pyenv, preventing you from using it directly. To solve this problem, first install the desired version `pyenv install 3.8.10` and then instead of the above command use this one: `pipenv --python %USERPROFILE%\.pyenv\pyenv-win\versions\3.8.10\python.exe install --dev`
3. The project is now ready to run.

<!-- USAGE EXAMPLES -->
## Usage

### Execution

Run the following instructions to launch the training and convert the model in a C compatible format:
   ```sh
   pipenv run prepare && pipenv run split && pipenv run train && pipenv run generate
   ```
The final model file will be located in: `output/model.cc`

There is also another way to create the model by using norms. This approach is not working well, so it's only a PoC implementation to show that it is not an acceptable solution. If you still want to use it, you can do the following:

<details>

   ```sh
   pipenv run prepare_norm && pipenv run split && pipenv run train_norm && pipenv run generate
   ```

</details>


<!-- TREE STRUCTURE -->
## Tree Structure
<details>

_TODO_

</details>

<!-- CREDITS -->
## Credits

Romain Monier [ [GitHub](https://github.com/rmonier) ] – Co-developer
<br>
Morgan Pelloux [ [GitHub](https://github.com/MonsieurSinge) ] – Co-developer
<br>
David Violes [ [GitHub](https://github.com/ViolesD) ] – Co-developer
<br>
Malik Sedira [ [GitHub](https://github.com/sediramalik) ] – Co-developer
<br>
Quentin Douarre [ [GitHub](https://github.com/Quintus618) ] – Co-developer
<br>
Noé Chauveau [ [GitHub](https://github.com/Noecv) ] – Co-developer
<br>
Pierre Favary [ [GitHub](https://github.com/pdf-0) ] – Co-developer

<!-- CONTACT -->
## Contact

Project Link : [https://github.com/PIR-IDS/wallet-model](https://github.com/PIR-IDS/wallet-model)

Organization Link : [https://github.com/PIR-IDS](https://github.com/PIR-IDS)
