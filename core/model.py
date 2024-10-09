import torch
import torch.nn as nn

class MusicTransformer(nn.Module):
    def __init__(self, vocab_size, embed_size, num_heads, num_layers, seq_length, dropout=0.1):
        super(MusicTransformer, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.pos_embedding = nn.Embedding(seq_length, embed_size)

        encoder_layer = nn.TransformerEncoderLayer(d_model=embed_size, nhead=num_heads, dropout=dropout)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)

        self.fc_out = nn.Linear(embed_size, vocab_size)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        seq_length, batch_size = x.shape[0], x.shape[1]
        pos = torch.arange(0, seq_length).unsqueeze(1).repeat(1, batch_size).to(x.device)

        embed = self.dropout(self.embedding(x) + self.pos_embedding(pos))
        transformer_out = self.transformer(embed)
        return self.fc_out(transformer_out)