#### Summa can summarize text, sometimes

How to use:

1. Setup [llama.cpp](https://github.com/ggerganov/llama.cpp)

```
  bash ./setup_model.sh
  cd llama.cpp
  make 
  cd ../
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
- [ ] Setup llama repo (as a submodule?)
- [ ] Speedup thing (deploy to the okayish machine?)
- [ ] Docker
- [ ] Improve summary readability
- [ ] ?Arch