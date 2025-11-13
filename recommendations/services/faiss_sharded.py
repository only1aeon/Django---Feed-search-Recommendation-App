import faiss, numpy as np, os
class ShardedFAISS:
    def __init__(self, dim, shard_paths=None):
        self.dim = dim
        self.shard_paths = shard_paths or []
        self.shards = []
        self.id_maps = []
        for p in self.shard_paths:
            self.shards.append(faiss.read_index(p))
            ids_file = p + '.ids.npy'
            if os.path.exists(ids_file):
                self.id_maps.append(np.load(ids_file, allow_pickle=True).tolist())
            else:
                self.id_maps.append([])
    def add_shard(self, index: faiss.Index, id_map: list, path: str):
        self.shards.append(index); self.id_maps.append(id_map); faiss.write_index(index, path); np.save(path + '.ids.npy', np.array(id_map, dtype=object)); self.shard_paths.append(path)
    def search(self, qvec, topk=50, nprobe=4):
        q = qvec.reshape(1,-1).astype('float32')
        results = []
        for idx, idmap in zip(self.shards, self.id_maps):
            idx.nprobe = nprobe
            D,I = idx.search(q, topk)
            for dist,pos in zip(D[0], I[0]):
                if pos<0 or pos>=len(idmap): continue
                results.append((idmap[pos], float(dist)))
        best = {}
        for (otype, oid), score in results:
            key=(otype,oid)
            if key not in best or score>best[key]: best[key]=score
        sorted_res = sorted(best.items(), key=lambda x:-x[1])[:topk]
        return [(k[1], v) for k,v in sorted_res]
