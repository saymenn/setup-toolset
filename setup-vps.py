import sys
import subprocess
import os
import time
import shutil

def initial_checks():
    current_user = os.getuid()
    current_shell = os.environ.get('SHELL', '').split('/')[-1]
    if current_user != 0:
        print("[X] fatal current user not root: ", current_user)
        sys.exit()
    else:
        print("[+] current user is root")
    if current_shell != "bash":
        print("[X] fatal current shell is not bash: ", current_shell)
        sys.exit()
    else:
        print("[+] current shell is bash")
    if shutil.which("git") is None:
        print("[-] git was not found, installing ...")
        time.sleep(2)
        try:
            subprocess.run(["sudo", "apt", "install", "-y", "git"], check=True)
        except subprocess.CalledProcessError as e:
            print("[X] fatal git couldn't install, try manually: ", e)
            sys.exit()
    else:
        print("[+] git is installed")
    if shutil.which("wget") is None:
        print("[-] wget was not found, installing ...")
        time.sleep(2)
        try:
            subprocess.run(["sudo", "apt", "install", "-y", "wget"], check=True)
        except subprocess.CalledProcessError as e:
            print("[X] fatal wget couldn't install, try manually: ", e)
            sys.exit()
    else:
        print("[+] wget is installed")
    if shutil.which("ruby") is None:
        print("[-] ruby was not found, installing ...")
        time.sleep(2)
        try:
            subprocess.run(["sudo", "apt", "install", "-y", "ruby"], check=True)
        except subprocess.CalledProcessError as e:
            print("[X] fatal ruby couldn't install, try manually: ", e)
            sys.exit() 
    else:
        print("[+] ruby is installed")        
    return True

def install_go():
    go_path = "/usr/local/go/bin/go"
    if not shutil.which("go") is None:
        print("[+] go is already installed")
        time.sleep(2)
    else:
        print("[+] installing golang ...")
        time.sleep(2)
        try:
            subprocess.run(["wget", "https://go.dev/dl/go1.24.2.linux-amd64.tar.gz"], check=True)
            print("\n[+] extracting go to /usr/local/go ...")
            time.sleep(2)
            subprocess.run(["tar", "-xvf", "go1.24.2.linux-amd64.tar.gz"], check=True)
            subprocess.run(["sudo", "mv", "go", "/usr/local"], check=True)
            print("\n[+] updating the ~/.bashrc file")
            time.sleep(2)
            with open(os.path.expanduser("~/.bashrc"), "a") as f:
                f.write("export PATH=$PATH:/usr/local/go/bin\n")
                f.write("export PATH=$PATH:/root/go/bin\n")
            time.sleep(2)
        except subprocess.CalledProcessError as e:
            print("[X] fatal golang couldn't download or install: ", e)
            sys.exit()
        
        print("[+] verfying go installation ...")
        time.sleep(2)
        if os.path.exists(go_path):
            print("[+] go is installed successfully")
        else:
            print("[X] fatal golang couldn't download or install")
            sys.exit()


def install_tools():
    # subfinder, assetfinder, amass, puredns, resolvers, dirsearch, ffuf, httpx, nuclei, naabu, tmux, gau, waybackurls, katana, qsreplace, uri_redirects.py, wpscan
    print("\n[+] preparing to install tools ...")
    time.sleep(2)
    try:
        print("[+] installing subfinder")
        subprocess.run(["go", "install", "-v", "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"], check=True)
        print("\n[+] installing assetfinder")
        subprocess.run(["go", "install", "-v", "github.com/tomnomnom/assetfinder@latest"], check=True)
        print("\n[+] installing amass")
        subprocess.run(["go", "install", "-v", "github.com/owasp-amass/amass/v4/...@latest"], check=True)
        print("\n[+] installing dirsearch")
        subprocess.run(["apt", "install", "-y", "dirsearch"], check=True)
        print("\n[+] installing ffuf")
        subprocess.run(["go", "install", "-v", "github.com/ffuf/ffuf/v2@latest"], check=True)
        print("\n[+] installing httpx")
        subprocess.run(["go", "install", "-v", "github.com/projectdiscovery/httpx/cmd/httpx@latest"], check=True)
        print("\n[+] installing nuclei")
        subprocess.run(["go", "install", "-v", "github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"], check=True)
        print("\n[+] installing naabu")
        subprocess.run(["apt", "install", "-y", "libpcap-dev"], check=True)
        subprocess.run(["go", "install", "-v", "github.com/projectdiscovery/naabu/v2/cmd/naabu@latest"], check=True)
        print("\n[+] installing gau")
        subprocess.run(["go", "install", "-v", "github.com/lc/gau/v2/cmd/gau@latest"], check=True)
        print("\n[+] installing waybackurls")
        subprocess.run(["go", "install", "-v", "github.com/tomnomnom/waybackurls@latest"], check=True)
        print("\n[+] installing katana")
        subprocess.run(["go", "install", "-v", "github.com/projectdiscovery/katana/cmd/katana@latest"], check=True)
        print("\n[+] installing qsreplace")
        subprocess.run(["go", "install", "-v", "github.com/tomnomnom/qsreplace@latest"], check=True)
        print("\n[+] installing /opt_redirect")
        if not os.path.exists("/opt/uri_redirect"):
            subprocess.run(["git", "clone", "https://github.com/saymenn/uri_redirect", "/opt/uri_redirect"], check=True)
        print("\n[+] installing tmux")
        subprocess.run(["apt", "install", "-y", "tmux"], check=True)
        print("\n[+] installing tricktest resolvers")
        if not os.path.exists("/opt/resolvers"):
            subprocess.run(["git", "clone", "https://github.com/trickest/resolvers", "/opt/resolvers"], check=True)
        print("\n[+] installing wpscan")
        subprocess.run(["apt", "install", "-y", "ruby-dev"], check=True)
        subprocess.run(["gem", "install", "wpscan"], check=True)
        print("\n[+] installing massdns")
        if not os.path.exists("/opt/massdns"):
            subprocess.run(["git", "clone", "https://github.com/blechschmidt/massdns", "/opt/massdns"], check=True)
            os.system("cd /opt/massdns;make;make install")
        print("\n[+] installing puredns")
        subprocess.run(["go", "install", "-v", "github.com/d3mondev/puredns/v2@latest"], check=True)
        print("\n[+] installing seclists")
        if not os.path.exists("/opt/seclists"):
            subprocess.run(["git", "clone", "https://github.com/danielmiessler/SecLists", "/opt/seclists"], check=True)
    except subprocess.CalledProcessError as e:
        print("[X] fatal one of the tools installation crashed: ", e)

    time.sleep(3)
    print("\n[+] verifying tools installation ...")
    tools_list = ["subfinder", "assetfinder", "amass", "puredns", "/opt/resolvers", "dirsearch", "ffuf", "httpx", "nuclei", "naabu", "tmux", "gau", "waybackurls", "katana", "qsreplace", "/opt/uri_redirect", "wpscan", "/opt/seclists"]
    for tool in tools_list:
        tool = tool.strip()
        if "/" in tool:
            if os.path.exists(tool):
                print(f"[+] {tool} is installed")
            else:
                print(f"[-] {tool} failed to install")
        else:
            if not shutil.which(tool) is None:
                print(f"[+] {tool} is installed")
            else:
                print(f"[-] {tool} failed to install")

if initial_checks():
    install_go()
    install_tools()
