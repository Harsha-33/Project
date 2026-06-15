# Run WeCareForYou on Ubuntu

This project is easiest to run on Ubuntu with Docker Compose. Docker keeps Angular, Flask, Nginx, and Python dependencies consistent across Windows and Linux.

## 1. Install Ubuntu Packages

If Docker is already installed, you can skip this section.

```bash
sudo apt update
sudo apt install -y ca-certificates curl git
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo tee /etc/apt/keyrings/docker.asc >/dev/null
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list >/dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker "$USER"
```

Log out and log in again after adding your user to the `docker` group.

## 2. Start The Project

```bash
git clone <your-repo-url> WeCareForYou
cd WeCareForYou
cp backend/.env.example backend/.env
nano backend/.env
```

Set your Supabase database URL in `backend/.env`.

Important: URL-encode special characters in the password. For example, `#` must be `%23`.

```env
SECRET_KEY=change-this
JWT_SECRET_KEY=change-this-too
DATABASE_URL=postgresql://postgres.<project-ref>:<password>@<pooler-host>:6543/postgres?sslmode=require
FLASK_DEBUG=false
```

Run:

```bash
chmod +x scripts/ubuntu-run.sh
./scripts/ubuntu-run.sh
```

Open:

- Frontend: `http://localhost:4200`
- Backend health: `http://localhost:5000/api/health`

Default admin login:

- Email: `admin@wecareforyou.com`
- Password: `Admin@123`

Useful commands:

```bash
docker compose ps
docker compose logs -f backend
docker compose logs -f frontend
docker compose down
docker compose up --build -d
```

# Jenkins Setup

Jenkins is a CI/CD server. For this project, Jenkins can automatically pull the code, build Angular, check Flask Python files, build Docker images, and deploy the containers on your Ubuntu machine.

## 1. Install Jenkins

```bash
sudo apt update
sudo apt install -y fontconfig openjdk-17-jre
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc >/dev/null
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list >/dev/null
sudo apt update
sudo apt install -y jenkins
sudo systemctl enable --now jenkins
```

Open Jenkins at `http://<ubuntu-server-ip>:8080`.

Get the first password:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Install suggested plugins.

## 2. Allow Jenkins To Use Docker

```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

## 3. Install Build Tools For Jenkins

```bash
sudo apt install -y nodejs npm python3
```

Node 20 is recommended for Angular 18. If Ubuntu installs an older Node version, install Node 20:

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

## 4. Add Jenkins Credentials

Go to `Manage Jenkins` -> `Credentials` -> `System` -> `Global credentials` -> `Add Credentials`.

Add these as `Secret text` credentials:

- ID: `wecare-database-url`
- ID: `wecare-secret-key`
- ID: `wecare-jwt-secret-key`

For `wecare-database-url`, paste your full Supabase PostgreSQL URL. Encode `#` as `%23`.

## 5. Create Jenkins Pipeline Job

1. Click `New Item`.
2. Choose `Pipeline`.
3. In `Pipeline`, choose `Pipeline script from SCM`.
4. Select Git.
5. Paste your repository URL.
6. Set branch to `*/main`.
7. Script path: `Jenkinsfile`.
8. Save and click `Build Now`.

The pipeline deploys only on the `main` branch. On other branches it builds and checks the project without replacing the running app.

## Troubleshooting

Check Jenkins logs:

```bash
sudo journalctl -u jenkins -f
```

Check app logs:

```bash
docker compose logs -f backend
docker compose logs -f frontend
```

If login fails after deployment, verify that `backend/.env` contains the correct `DATABASE_URL` and that the Supabase password is URL-encoded.
