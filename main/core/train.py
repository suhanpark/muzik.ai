import torch

def train(model, device, dataloader, criterion, optimizer, num_epochs):
    for epoch in range(num_epochs):
        model.train()
        epoch_loss = 0

        for batch, (x, y) in enumerate(dataloader):
            x, y = x.to(device), y.to(device)

            # Forward pass
            output = model(x)
            loss = criterion(output.permute(1, 2, 0), y.permute(1, 0))

            # Backward pass and optimization
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()

        print(f'\nEpoch {epoch+1}/{num_epochs}, Loss: {epoch_loss/len(dataloader)}')

    model_save_path = f'{content_dir}/muzik_transformer.pth'
    torch.save(model.state_dict(), model_save_path)

    print(f"Model saved at {model_save_path}")
    print("Training complete!")