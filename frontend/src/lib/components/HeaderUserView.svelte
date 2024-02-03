<script lang="ts">
    let isLoggedIn : Boolean = true;
    let username : string = "GlizzMeister";
    let userPfp : string = "https://static-cdn.jtvnw.net/jtv_user_pictures/6c45032c-a049-46c7-bfc9-f9ac2fc8c47e-profile_image-70x70.png"//"https://static-cdn.jtvnw.net/jtv_user_pictures/d57c1c0d-31da-4722-ab41-8c8673a0ba4a-profile_image-70x70.png";//
</script>

<div class="text-zinc-300">
    {#if isLoggedIn}
    <div class="flex flex-row items-center space-x-2">
        <span>{username}</span>
        <img src={userPfp} class="rounded-full border-solid border-2 border-white object-fill h-10" alt="The user's twitch profile."/>
    </div>
    <!-- This is where the dropdown goes, that has more settings. -->
    {:else}
    <button class="bg-purple-600 rounded p-3">Login via Twitch</button>
    {/if}
</div>