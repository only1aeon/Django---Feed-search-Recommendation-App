from django.core.management.base import BaseCommand
from recommendations.models import Video, Embedding
from recommendations.services.embedding import encode_texts
import numpy as np, faiss, os
class Command(BaseCommand):
    help='Index videos into FAISS shard (dev single shard)'
    def handle(self,*args,**options):
        dim=512; pks=[]; vecs=[]
        for v in Video.objects.all():
            text = (v.title or '') + ' ' + ' '.join(v.tags or [])
            vec = encode_texts([text])[0]
            pks.append(('video', v.pk)); vecs.append(vec)
            b = vec.astype('float32').tobytes()
            Embedding.objects.update_or_create(owner_type='video', owner_id=v.pk, defaults={'vector':b,'dim':dim})
        if vecs:
            arr = np.stack(vecs,axis=0).astype('float32')
            index = faiss.IndexFlatIP(dim)
            faiss.normalize_L2(arr)
            index.add(arr)
            faiss.write_index(index, '/tmp/faiss.index')
            np.save('/tmp/faiss.index.ids.npy', np.array(pks, dtype=object))
            self.stdout.write(f'Indexed {len(vecs)} videos')
