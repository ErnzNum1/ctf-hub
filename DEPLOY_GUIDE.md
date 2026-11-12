# CTF Hub: VirtualBox + Ubuntu + VS Code SSH + Docker + paglipat sa ibang computer

Sundin ang mga hakbang **ayon sa pagkakasunod**. Bawat hakbang may "Dapat mong makita" para alam mo kung tama.

Sa guide na ito:
- **Windows** = ang computer mo ngayon (PowerShell, VS Code, VirtualBox).
- **VM** = ang Ubuntu na tumatakbo sa loob ng VirtualBox.
- `USERNAME` = ang username na gagawin mo sa Ubuntu (halimbawa `ctf`). Palitan mo ito kapag nakita mo.

---

## Hakbang 1: SQLite (tapos na)

Hindi mo na kailangang i-connect ang SQLite. Nasa `app.py` na ito at awtomatiko:
- Pagtakbo ng app, gagawin nito ang file na `ctf.db` (ito ang database) kung wala pa.
- Nandoon ang users, progress ng challenges, mga video at ang text ng pages.

Walang ibang file na kailangan. Kumpleto na ang project mo.

---

## Hakbang 2: Gumawa ng Ubuntu VM sa VirtualBox

### 2.1 I-download
1. VirtualBox: https://www.virtualbox.org/wiki/Downloads → **Windows hosts**. I-install (Next, Next, Finish).
2. Ubuntu Server ISO: https://releases.ubuntu.com/24.04.5/ubuntu-24.04.5-live-server-amd64.iso (mga 2 GB).

### 2.2 Gumawa ng VM
1. Buksan ang VirtualBox → **New**.
2. **Name:** `ctfhub`. **ISO Image:** piliin ang na-download na ISO. Lagyan ng check ang **Skip Unattended Installation**. **Next**.
3. **Base Memory:** `4096` MB. **Processors:** `2`. **Next**.
4. **Virtual Hard Disk:** `30 GB`. **Huwag** lagyan ng check ang "Pre-Allocate Full Size" (para dynamic at puwedeng paliitin). **Next** → **Finish**.

### 2.3 Port forwarding (para makapasok ang VS Code at browser mo)
1. Piliin ang `ctfhub` → **Settings** → **Network**.
2. **Adapter 1** = **NAT** → pindutin ang **Advanced** → **Port Forwarding**.
3. Pindutin ang **+** at gumawa ng 2 rule:

| Name | Protocol | Host IP | Host Port | Guest IP | Guest Port |
|---|---|---|---|---|---|
| ssh | TCP | 127.0.0.1 | 2222 | (iwan blangko) | 22 |
| web | TCP | 127.0.0.1 | 8000 | (iwan blangko) | 8000 |

4. **OK** → **OK**.

### 2.4 I-install ang Ubuntu
Pindutin ang **Start**. Sa loob ng VM, mouse ay minsan hindi gagana; gamitin ang **Enter**, **arrow keys** at **Space**.

1. Language: **English** → Enter.
2. Kung may "Update installer", piliin **Continue without updating**.
3. Keyboard: Enter (**Done**).
4. Type of install: **Ubuntu Server** → **Done**.
5. Network: Enter (**Done**). Dapat may IP address (halimbawa `10.0.2.15`).
6. Proxy: **Done** (blangko).
7. Mirror: **Done**.
8. Storage: **Use an entire disk** (default) → **Done** → **Done** → **Continue**.
9. Profile setup:
   - Your name: kahit ano
   - Your server's name: `ctfhub`
   - Username: `ctf` (ito ang `USERNAME`)
   - Password: piliin mo at **isulat mo**
10. Ubuntu Pro: **Skip** → Continue.
11. **SSH:** lagyan ng check ang **Install OpenSSH server** gamit ang **Space**, tapos **Done**. (Kailangan ito para sa VS Code.)
12. Featured snaps: **Done** (huwag pumili ng kahit ano).
13. Hintayin matapos. Kapag lumabas ang **Reboot Now**, pindutin ang Enter.
14. Kung may "Please remove the installation medium", pindutin lang ang Enter.

**Dapat mong makita:** `ctfhub login:`. I-type ang `ctf`, Enter, tapos ang password (hindi lalabas ang tina-type mo, normal iyon).

### 2.5 I-update ang Ubuntu
Sa loob ng VM:
```
sudo apt update && sudo apt upgrade -y
```
Kapag nagtanong, i-type ang password, Enter.

---

## Hakbang 3: I-connect ang VS Code (SSH)

1. Sa VS Code, pindutin ang **Extensions** (Ctrl+Shift+X), hanapin ang **Remote - SSH** (ng Microsoft), **Install**.
2. Pindutin ang **Ctrl+Shift+P**, i-type ang `Remote-SSH: Connect to Host...`, Enter.
3. Piliin **Add New SSH Host** at i-type:
   ```
   ssh -p 2222 USERNAME@127.0.0.1
   ```
   (Palitan ang `USERNAME`, halimbawa `ssh -p 2222 ctf@127.0.0.1`.) Piliin ang unang config file.
4. Pindutin ang **Connect** sa lumabas na kahon. Piliin **Linux**, tapos **Continue** sa fingerprint, tapos i-type ang password.

**Dapat mong makita:** sa kaliwang ibaba ng VS Code, berdeng `SSH: 127.0.0.1`.

### 3.1 Ilipat ang project sa VM
Buksan ang **PowerShell** sa Windows. Una, **huwag isama ang `venv`**: i-rename muna ang `venv` folder sa labas, o burahin ito (hindi ito gagana sa Linux at hindi na kailangan).

```
scp -P 2222 -r "C:\Users\Admin\OneDrive\Desktop\CAPTURE THE FLAG\ctf_site" USERNAME@127.0.0.1:~/
```

Kapag may nagtanong na "continue connecting", i-type ang `yes`, tapos password. Mga video mo ay kasama kaya puwedeng matagalan.

### 3.2 Buksan ang folder sa VS Code
**File → Open Folder** → `/home/USERNAME/ctf_site` → **OK**.

### Makakapag-edit ka pa ba ng code?
**Oo.** Ine-edit mo ang mga file sa mismong VM, gaya ng dati. Pagkatapos ng Docker (Hakbang 5):
- **Code** (`.py`, `.html`): i-save, tapos patakbuhin ang `docker compose up -d --build` para ma-apply.
- **Admin page** (edit ng text, mag-upload ng video, users, progress): **walang rebuild**, kasi nasa database at sa folder na `static/videos`.

---

## Hakbang 4: I-install ang Docker (sa VM)

### Ano ang Docker, sa simpleng salita
- **Image** = nakabalot na kopya ng app mo kasama ang Python at lahat ng kailangan.
- **Container** = ang image na tumatakbo. Para siyang maliit na computer sa loob ng VM.
- **Dockerfile** = ang recipe kung paano gawin ang image. (Nasa project mo na.)
- **docker-compose.yml** = ang file na nagsasabi kung paano ito pa-patakbuhin (port, folders). (Nasa project mo na.)
- **Volume** = folder sa VM na ibinabahagi sa container para hindi mawala ang database at mga video kapag nire-rebuild.

Ang benepisyo: tatakbo ang parehong app sa kahit anong computer na may Docker.

### 4.1 Mag-install
I-paste ang mga ito sa terminal ng VS Code (**Terminal → New Terminal**, na nasa VM). Isa-isang block:

```
sudo apt update
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```
```
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 4.2 Payagan ang user mo (para hindi laging `sudo`)
```
sudo usermod -aG docker $USER
```
Tapos **i-disconnect at i-connect ulit ang VS Code** (Ctrl+Shift+P → `Remote-SSH: Close Remote Connection`, tapos connect ulit), para magka-bisa.

### 4.3 Subukan
```
docker run hello-world
```
**Dapat mong makita:** "Hello from Docker!"

---

## Hakbang 5: Patakbuhin ang CTF Hub gamit ang Docker

Sa terminal ng VS Code (nasa VM):

```
cd ~/ctf_site
mkdir -p data static/videos
docker compose up -d --build
```

Ang una ay matagal (nagda-download ng Python). Tingnan kung tumatakbo:
```
docker compose ps
```
**Dapat mong makita:** `ctf-hub` na `Up`.

Buksan sa **browser ng Windows**: **http://localhost:8000**

Mga kapaki-pakinabang na command:

| Gusto mo | Command |
|---|---|
| Tingnan ang mensahe/error ng app | `docker compose logs --tail 50` |
| Ihinto | `docker compose down` |
| I-apply ang binago mong code | `docker compose up -d --build` |
| I-restart lang | `docker compose restart` |

Awtomatiko itong magsisimula ulit kapag nag-reboot ang VM (`restart: unless-stopped`).

### Mahalaga
- **Palitan ang password** ng `capturetheflag` (admin) at `ubuntu` sa **Account** page, lalo na kung ipapakita mo ang site sa iba.
- Ang database ay nasa `~/ctf_site/data/ctf.db`. Ang mga video ay nasa `~/ctf_site/static/videos`.
- Kung gusto mong dalhin ang dati mong database mula sa Windows: kopyahin ang `ctf.db` sa `data/` **bago** ang unang `docker compose up`.

---

## Hakbang 6: Ilipat sa hard drive at sa ibang computer

May dalawang paraan. Ang **Paraan B ay mas maliit at mas madali**.

### Paraan A: Buong VM (.ova)

**6A.1 Paliitin muna ang VM.** Sa VM:
```
cd ~/ctf_site
docker compose down
sudo apt clean
sudo journalctl --vacuum-size=50M
docker image prune -f
```
(Kung may mga `.mkv` na kopya sa `static/videos` na hindi mo ginagamit, burahin mo na rin.)

Tapos "i-zero" ang libreng espasyo, para mabawasan ng compact ang laki:
```
sudo dd if=/dev/zero of=/zerofile bs=1M status=progress
sudo rm /zerofile
```
Normal na lalabas ang `No space left on device`. Pagkatapos:
```
sudo poweroff
```

**6A.2 I-compact ang disk (Windows PowerShell):**
```
cd "C:\Program Files\Oracle\VirtualBox"
.\VBoxManage.exe modifymedium disk "C:\Users\Admin\VirtualBox VMs\ctfhub\ctfhub.vdi" --compact
```
Kung hindi tugma ang path, sa VirtualBox: **File → Tools → Virtual Media Manager** at tingnan ang location ng disk.

**6A.3 I-export:** VirtualBox → **File → Export Appliance** → piliin `ctfhub` → Next → **Format: OVF 2.0**, **File:** `ctfhub.ova` sa hard drive mo → **Finish**.

> **Babala sa hard drive:** kung FAT32 ang format ng drive, hindi ito tatanggap ng file na lampas 4 GB. Gamitin ang **exFAT** o **NTFS**. (Kung blangko ang drive: Right-click sa drive → Format → exFAT. Buburahin nito ang laman.)

**6A.4 Sa ibang computer** (Windows o Ubuntu): i-install ang VirtualBox, tapos **File → Import Appliance** → piliin ang `.ova` → **Finish** → **Start**. Ang port forwarding (2222 at 8000) ay kasama na; buksan lang ang `http://localhost:8000` at gamitin ang VS Code SSH gaya ng Hakbang 3. Dapat pa ring `Up` ang app (restart policy).

### Paraan B: Folder lang + Docker (mas maliit)
Sa VM, i-zip ang project at ilipat sa Windows:
```
cd ~
zip -r ctf_site.zip ctf_site
```
(Kung walang zip: `sudo apt install -y zip`.) Kunin ito sa Windows:
```
scp -P 2222 USERNAME@127.0.0.1:~/ctf_site.zip .
```
Ilagay sa hard drive. Sa ibang computer na may Docker (Docker Desktop sa Windows, o Hakbang 4 sa Ubuntu): i-unzip, buksan ang terminal sa folder, at:
```
docker compose up -d --build
```
Buksan ang http://localhost:8000. Kasama ang database at mga video dahil nasa loob ng folder ang `data/` at `static/videos/`.

---

## Kapag may problema

| Problema | Ayusin |
|---|---|
| VS Code: "Connection refused" | Naka-on ba ang VM? Tama ba ang port forwarding (2222 → 22)? Naka-install ba ang OpenSSH (Hakbang 2.4 #11)? |
| VS Code: "REMOTE HOST IDENTIFICATION HAS CHANGED" | Burahin ang linyang `[127.0.0.1]:2222` sa `C:\Users\Admin\.ssh\known_hosts`, subukan ulit |
| `permission denied` sa docker | Hindi pa nag-reconnect pagkatapos ng `usermod`. I-reconnect, o i-reboot ang VM |
| Hindi mabuksan ang http://localhost:8000 | `docker compose ps` at `docker compose logs`. Naka-set ba ang `web` port forwarding (8000 → 8000)? |
| Error na `unable to open database file` / `Permission denied` sa `data` | `sudo chown -R 1000:1000 data static/videos` tapos `docker compose restart` |
| Walang lumalabas na video | Nasa `static/videos` ba ang file, at pareho ang pangalan sa `seed_data.py`? Tingnan ang `docker compose logs` para sa "video file not found" |
| Naubusan ng espasyo ang VM | `docker image prune -f`, `sudo apt clean`, burahin ang mga hindi kailangang video |
