# BoltR Health Check & Toolchain Verification

After BoltR is running (`make up` and all containers are healthy), verify the recon toolchain:

```bash
cd /path/to/boltr
./scripts/health_check.sh
```

This checks that **nuclei**, **naabu**, **subfinder**, **amass**, and **httpx** are installed and executable inside the Celery container.

## Manual checks (optional)

```bash
# List running containers
docker compose -f docker/docker-compose.yml ps

# Run tool checks inside the Celery container
docker exec rengine-celery-1 nuclei -version
docker exec rengine-celery-1 naabu -version
docker exec rengine-celery-1 subfinder -version
docker exec rengine-celery-1 amass -version
docker exec rengine-celery-1 httpx -version
```

## If installation failed: "No space left on device"

The Postgres container needs disk space to create its data directory. Free space and retry:

```bash
# Check disk usage
df -h
docker system df

# Free space (examples)
docker system prune -f
docker volume prune -f   # only if you have no important volumes
# Then run the installer again:
sudo env SUDO_USER=kali ./install.sh -n
```

After a successful `make up`, run `./scripts/health_check.sh` to confirm the toolchain.
