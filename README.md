#### Summa can summarize text, sometimes

How to use:

1. Setup [llama.cpp](https://github.com/ggerganov/llama.cpp)

```
  git submodule update --init --recursive 
  cd llama.cpp
  make 
  cd ../
  bash ./setup_model.sh
```

2. Install simple stuff
```
  pipenv shell
  pipenv install
```

3. Run thing

```
flask run
```


#### TODO

- [x] Reliable queue on the client
- [x] Setup llama repo as a submodule
- [ ] Speedup thing (deploy to the okayish machine?)
- [ ] Docker
- [ ] Improve summary readability
- [ ] ?Arch