    // Cards width needs to be removed in order to fit them inside grid equally.
    
    <>
      <div className="bg-[#0F0F0F] py-20 px-4 lg:px-48 flex flex-col gap-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <ProfileCard />
          <div className="grid grid-cols-1 gap-6">
            <div className="">
              <StripCard />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 ">
              <SecondaryCard
                imageSrc="/sign.png"
                imageAlt="My Works"
                description="more about me"
                title="Credentials"
              />
              <SecondaryCard
                imageSrc="/my-works.png"
                imageAlt="My Works"
                description="Showcase"
                title="Projects"
              />
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 md:gap-x-6 gap-y-6	">
          <SecondaryCard
            imageSrc="/gfonts.png"
            imageAlt="My Works"
            description="blog"
            title="Gfonts"
          />
          <div className="col-span-2">
            <ServicesCard />
          </div>
          <SecondaryCard
            imageSrc="/social.jpg"
            imageAlt="My Works"
            description="STAY WITH ME"
            title="Profiles"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <ExperienceCard />
          <WorkTogetherCard />
        </div>
      </div>
    </>