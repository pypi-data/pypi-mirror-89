from thespian.actors import ActorSystem, Actor, ValidateSource, ValidatedSource
import sys

if __name__ == "__main__":
    portnum = int(sys.argv[1])

    asys = ActorSystem('multiprocTCPBase', {'Admin Port': portnum})
    print(asys.loadActorSource('src.zip'))
