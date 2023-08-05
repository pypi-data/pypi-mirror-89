import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.metrics import *
import numpy as np

class Trainer(object):
    def __init__(self,model_name,
                 model,
                 train_loader,
                 dev_loader,
                 test_loader,
                 optimizer,
                 loss_fn,
                 save_path,
                 epochs,
                 writer,
                 max_norm,
                 eval_step_interval):
        super(Trainer, self).__init__()

        self.model_name=model_name.lower()
        self.model = model
        self.train_loader = train_loader
        self.dev_loader = dev_loader
        self.test_loader = test_loader
        self.optimizer = optimizer
        self.loss_fn = loss_fn
        self.save_path = save_path
        self.epochs = epochs
        self.writer = writer
        self.max_norm = max_norm
        self.step_interval = eval_step_interval

    def train(self):
        self.model.train()
        self.best_f1 = 0.0
        global_steps = 1

        for epoch in range(1, self.epochs + 1):
            for idx, batch_data in enumerate(self.train_loader, start=1):

                if self.model_name in ["textcnn","rcnn","han","dpcnn"]:
                    input_ids,y_true=batch_data[0],batch_data[1]
                    logits=self.model(input_ids)
                elif self.model_name in ["berttextcnn","bertrcnn","berthan","bertdpcnn"]:
                    if len(batch_data)==3:
                        input_ids,attention_mask,y_true=batch_data[0],batch_data[1],batch_data[2]
                        logits=self.model(input_ids,attention_mask)
                    else:
                        input_ids,y_true=batch_data[0],batch_data[1]
                        logits=self.model(input_ids)

                else:
                    raise ValueError("the number of batch_data is wrong!")

                loss = self.loss_fn(logits, y_true)
                if self.writer is not None:
                    self.writer.add_scalar("train/loss", loss.item(), global_step=global_steps)
                print(
                    "epoch:{epoch},step:{step},train_loss:{loss}.".format(epoch=epoch, step=idx, loss=loss.item()))

                self.optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=self.max_norm)
                self.optimizer.step()

                global_steps += 1

                if global_steps % self.step_interval == 0:
                    p, r, f1 = self.eval()
                    if self.writer is not None:
                        self.writer.add_scalar("valid/p", p, global_steps)
                        self.writer.add_scalar("valid/r", r, global_steps)
                        self.writer.add_scalar("valid/f1", f1, global_steps)
                    print("------start evaluating model in dev data------")
                    print(
                        "epoch:{epoch},step:{idx},precision:{p},recall:{r},F1-score:{f1}".format(epoch=epoch,
                                                                                                       idx=idx, p=p,
                                                                                                       r=r, f1=f1))
                    if self.best_f1 < f1:
                        self.best_f1 = f1
                        torch.save(self.model.state_dict(), f=self.save_path)

                    print("epoch:{epoch},step:{idx},best_f1:{best_f1}".format(epoch=epoch, idx=idx,
                                                                                     best_f1=self.best_f1))
                    print("------finish evaluating model in dev data------")
                    self.model.train()

        if self.writer is not None:
            self.writer.flush()
            self.writer.close()

    def eval(self):
        self.model.eval()
        y_preds = []
        y_trues=[]

        with torch.no_grad():
            for idx, batch_data in enumerate(self.dev_loader, start=1):

                if self.model_name in ["textcnn","rcnn","han","dpcnn"]:
                    input_ids,y_true=batch_data[0],batch_data[1]
                    logits=self.model(input_ids)
                elif self.model_name in ["berttextcnn","bertrcnn","berthan","bertdpcnn"]:
                    input_ids,attention_mask,y_true=batch_data[0],batch_data[1],batch_data[2]
                    logits=self.model(input_ids,attention_mask)
                else:
                    raise ValueError("the number of batch_data is wrong!")

                y_true=list(y_true.cpu().numpy())
                y_trues.extend(y_true)

                logits=logits.cpu().numpy()
                for item in logits:
                    pred=np.argmax(item)
                    y_preds.append(pred)

        y_preds=np.array(y_preds)
        y_trues=np.array(y_trues)

        p=precision_score(y_trues,y_preds,average="macro")
        r=recall_score(y_trues,y_preds,average="macro")
        f1=f1_score(y_trues,y_preds,average="weighted")

        return p,r,f1

    def test(self):
        self.model.eval()
        y_preds = []
        y_trues=[]

        with torch.no_grad():
            for idx, batch_data in enumerate(self.test_loader, start=1):

                if self.model_name in ["textcnn","rcnn","han","dpcnn"]:
                    input_ids,y_true=batch_data[0],batch_data[1]
                    logits=self.model(input_ids)
                elif self.model_name in ["berttextcnn","bertrcnn","berthan","bertdpcnn"]:
                    input_ids,attention_mask,y_true=batch_data[0],batch_data[1],batch_data[2]
                    logits=self.model(input_ids,attention_mask)
                else:
                    raise ValueError("the number of batch_data is wrong!")

                y_true=list(y_true.cpu().numpy())
                y_trues.extend(y_true)

                logits=logits.cpu().numpy()
                for item in logits:
                    pred=np.argmax(item)
                    y_preds.append(pred)

        y_preds=np.array(y_preds)
        y_trues=np.array(y_trues)

        p=precision_score(y_trues,y_preds,average="macro")
        r=recall_score(y_trues,y_preds,average="macro")
        f1=f1_score(y_trues,y_preds,average="weighted")

        return p,r,f1

    def predict(self,x):
        self.model.eval()
        y_preds=[]
        with torch.no_grad():
            for idx, batch_data in enumerate(x, start=1):
                if self.model_name in ["textcnn","rcnn","han","dpcnn"]:
                    input_ids=batch_data
                    logits=self.model(input_ids)
                elif self.model_name in ["berttextcnn","bertrcnn","berthan","bertdpcnn"]:
                    input_ids,attention_mask=batch_data[0],batch_data[1]
                    logits=self.model(input_ids,attention_mask)
                else:
                    raise ValueError("the number of batch_data is wrong!")

                logits=logits.cpu()
                prob=F.softmax(logits,dim=-1)
                y_preds.extend(prob)

        y_preds=torch.stack(y_preds,dim=0).numpy()
        return y_preds




