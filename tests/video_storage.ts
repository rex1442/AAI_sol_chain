import * as anchor from "@coral-xyz/anchor";
import { Program } from "@coral-xyz/anchor";
import { VideoStorage } from "../target/types/video_storage";
import { assert } from "chai";

describe("video_storage", () => {
  // Configure the client to use the local cluster.
  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);

  //bring program instance
  const program = anchor.workspace.VideoStorage as Program<VideoStorage>;

  // Define accounts and other necessary variables
  const videoInfoAccount = anchor.web3.Keypair.generate();
  const videoDate = "2023-06-01";
  const device = "Camera123";
  const location = "Seoul";
  const user = "user123";
  const hash = "somehashvalue"; // Normally you'd generate this dynamically

  // initialize test
  it("Is initialized!", async () => {
    // Initialize the video storage
    const tx = await program.methods.initialize().rpc();
    console.log("Your transaction signature", tx);
  });

  it("Stores video info", async () => {
    // Test storing video info
    const tx = await program.methods
      .storeVideoInfo(videoDate, device, location, user, hash)
      .accounts({
        videoInfo: videoInfoAccount.publicKey,
        user: provider.wallet.publicKey,
        systemProgram: anchor.web3.SystemProgram.programId,
      })
      .signers([videoInfoAccount])
      .rpc();
    console.log("Your transaction signature", tx);

    // Fetch the account and assert the stored values
    const account = await program.account.videoInfo.fetch(
      videoInfoAccount.publicKey
    );
    assert.equal(account.videoDate, videoDate);
    assert.equal(account.device, device);
    assert.equal(account.location, location);
    assert.equal(account.user, user);
    assert.equal(account.hash, hash);
  });
});
