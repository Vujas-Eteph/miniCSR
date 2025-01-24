# Check Server Resources (CSR) - Minimalist Version

*In a computer science lab or tech company, managing multiple servers and GPUs for deep learning experiments can be challenging. miniCSR provides a minimalist and private webpage to monitor the resources of local 'GPU servers.' Only you and authorized users within your network can access this webpage, offering a secure way to view detailed statistics of your GPU, CPU, and disk space resources for each server—all in one place.*

Here's an anonymized screenshot of how it looks:
![CSR_output_anonymized](./assets/Anonymized_CSR_output.png)

## Setting up miniCSR

### Clone the project
Run the following on your local machine that is doing the monitoring:  
```bash
git clone https://github.com/Vujas-Eteph/miniCSR
mamba env create -f environment.yml  # You can also use conda instead of mamba (or update the environement instead)
```
> [!NOTE]  
> We don't need to install anything on the servers that we are going to monitor, since we only rely on basic linux commands that should already be available natively.

### Configuration of the servers to access with miniCSR 
- Step 1 (Optional): When setting up ssh connections, natively linux will save it in .ssh/config, which you can modify like below. However, you can skip this if you don't want to miggle with you current ssh configs.
    ```yaml
    # .ssh/config template
    Host SERVER_ALIAS
        HostName SERVER_IP  # Replace with actual server IP
        User USER_NAME      # Replace with actual user name
        IdentityFile ~/.ssh/id_rsa
        Port XX             # Replace with the actual port number
        UserKnownHostsFile ~/.ssh/known_hosts
    ```
- Step 2: Add the **SERVER_ALIAS** entries for the servers you want to monitor in the [**server_names.yaml**](./config/server_names.yaml) file. You can refer to this [example configuration](./config/example_server_names.yaml) for guidance on setting it up your **server_names.yaml**. Using this allows you to only monitor servers you are interested in, and not every server you have ssh access to.

### Running miniCSR

- Run the following commands in TMUX:
    ```bash
    tmux new-session CSR
    mamba activate miniCSR
    bash ./start_CSR.sh
    ```
> [!NOTE]
> By default, the webpage is on your **local port 1990**. You can change that in the configurations.

> [!WARNING] 
> This project has been tested on an Ubuntu distributions and uses Python 3. We mostly rely on basic linux commands to get the internal state of the servers and process it with Python. 

---

## Motivation for the project
Before CSR, I had to manually check if a server was available by SSHing into each server one by one. This process became cumbersome already at the second attempt.  
So to **save time**, I wanted a centralized monitoring tool that consolidates this task, making it quick and efficient. Hence, this project.  
