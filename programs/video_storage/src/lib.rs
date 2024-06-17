use anchor_lang::prelude::*;

declare_id!("YourProgramIdHere");

#[program]
pub mod video_storage {
    use super::*;

    pub fn store_video_info(
        ctx: Context<StoreVideoInfo>, 
        video_date: String, 
        device: String, 
        location: String, 
        user: String, 
        hash: String
    ) -> Result<()> {
        let video_info = &mut ctx.accounts.video_info;
        video_info.video_date = video_date;
        video_info.device = device;
        video_info.location = location;
        video_info.user = user;
        video_info.hash = hash;
        Ok(())
    }
}

#[derive(Accounts)]
pub struct StoreVideoInfo<'info> {
    #[account(init, payer = user, space = 8 + 32 * 4 + 64)]
    pub video_info: Account<'info, VideoInfo>,
    #[account(mut)]
    pub user: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[account]
pub struct VideoInfo {
    pub video_date: String,
    pub device: String,
    pub location: String,
    pub user: String,
    pub hash: String,
}
