# A minimal SSH server for practicing remote connections
FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y openssh-server && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir /run/sshd

# Create a user called "inzva" with a home directory
RUN useradd -m -s /bin/bash inzva && \
    mkdir -p /home/inzva/.ssh && \
    chmod 700 /home/inzva/.ssh && \
    chown -R inzva:inzva /home/inzva/.ssh

# Add a welcome message
RUN echo '\n\
  ╔════════════════════════════════════════════╗\n\
  ║  🎉 Welcome to the inzva remote server!   ║\n\
  ║  You connected via SSH — well done!        ║\n\
  ║  Type "exit" to disconnect.                ║\n\
  ╚════════════════════════════════════════════╝\n' > /home/inzva/.motd && \
    echo 'cat ~/.motd' >> /home/inzva/.bashrc

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
