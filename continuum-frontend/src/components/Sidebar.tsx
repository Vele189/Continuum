import { useMemo, useState } from "react";


type TreeProject = {
  id: string;
  name: string;
  children?: { id: string; name: string }[];
};

const treeProjects: TreeProject[] = [
  { id: "p1", name: "Untitled long project_na..." },
  {
    id: "p2",
    name: "Untitled long project_na...",
    children: [{ id: "c1", name: "UX Strategy" }],
  },
];

const Sidebar = () => {
  const [search, setSearch] = useState("");
  const [selectedParentId, setSelectedParentId] = useState<string>(
    treeProjects[1]?.id ?? "p2"
  );
  const [selectedChildId, setSelectedChildId] = useState<string>(
    treeProjects[1]?.children?.[0]?.id ?? "c1"
  );
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);

  const filteredParents = useMemo(() => {
    const q = search.trim().toLowerCase();
    if (!q) return treeProjects;

    return treeProjects
      .map((p) => {
        const parentMatch = p.name.toLowerCase().includes(q);
        const kids = p.children ?? [];
        const filteredKids = kids.filter((c) =>
          c.name.toLowerCase().includes(q)
        );

        if (parentMatch) return p;
        if (filteredKids.length > 0) return { ...p, children: filteredKids };
        return null;
      })
      .filter(Boolean) as TreeProject[];
  }, [search]);

  return (
   

    <aside className="w-[212px] min-h-[962px] bg-[#F7FBFF] border-r border-[#E9EEF5] flex flex-col justify-between shrink-0">
      {/* TOP SECTION */}
      
      <div className="w-[212px] flex flex-col px-[12px] pt-[24px] pb-[16px] gap-[20px]">
        {/* LOGO  */}
        <div className="w-full flex items-center justify-center pb-[4px]">
          <img
            src="/icons/Continuum (1).svg"
            alt="Continuum"
            className="w-[174px] h-[30px] object-contain"
          />
        </div>

        {/* SEARCH  */}
        <div className="w-full h-[40px] rounded-full bg-[#EFF4FA] border border-[#E9EEF5] flex items-center gap-[8px] px-[12px]">
          <img
            src="/icons/search.svg"
            alt=""
            className="w-[14px] h-[14px] opacity-70"
          />
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search Projects"
            className="w-full bg-transparent outline-none text-[13px] text-[#0B191F] placeholder:text-[#64748B]"
          />
        </div>

        {/* NAV ICONS ROW  */}
        <div className="w-full flex gap-[8px]">
          <button
            type="button"
            title="Home"
            className="w-[47px] h-[40px] rounded-[8px] bg-[#EEF3F8] border border-[#E9EEF5] flex items-center justify-center"
          >
            <img src="/icons/house.svg" alt="" className="w-[16px] h-[16px]" />
          </button>

          <button
            type="button"
            title="Invoice"
            className="w-[47px] h-[40px] rounded-[8px] bg-[#EEF3F8] border border-[#E9EEF5] flex items-center justify-center"
          >
            <img
              src="/icons/scroll-text.svg"
              alt=""
              className="w-[16px] h-[16px]"
            />
          </button>

          <button
            type="button"
            title="Assigned to Me"
            className="w-[47px] h-[40px] rounded-[8px] bg-[#EEF3F8] border border-[#E9EEF5] flex items-center justify-center"
          >
            <img
              src="/icons/target.svg"
              alt=""
              className="w-[16px] h-[16px]"
            />
          </button>

          <button
            type="button"
            title="Created by Me"
            className="w-[47px] h-[40px] rounded-[8px] bg-[#EEF3F8] border border-[#E9EEF5] flex items-center justify-center"
          >
            <img src="/icons/list.svg" alt="" className="w-[16px] h-[16px]" />
          </button>
        </div>

        {/* PROJECTS HEADER  */}
        <div className="w-full flex items-center justify-between pt-[4px]">
          <p className="text-[14px] font-medium leading-[14px] text-[#606D76]">
            Projects
          </p>

          <div className="flex items-center gap-[8px]">
            <button
              type="button"
              className="w-[24px] h-[24px] flex items-center justify-center"
              title="More"
            >
              <img
                src="/icons/Ellepsis.svg"
                alt="More"
                className="w-[16px] h-[16px]"
              />
            </button>

            <button
              type="button"
              className="w-[24px] h-[24px] flex items-center justify-center"
              title="Add"
            >
              <img
                src="/icons/Add.svg"
                alt="Add"
                className="w-[16px] h-[16px]"
              />
            </button>
          </div>
        </div>
      </div>
      

      {/* PROJECT LIST */}
      <div className="w-[212px] flex-1 overflow-y-auto px-[12px]">
        <div className="flex flex-col gap-[4px]">
          {filteredParents.map((p) => {
            const parentSelected = p.id === selectedParentId;

            return (
              <div key={p.id} className="w-full">
                {/* PARENT ROW */}
                <button
                  type="button"
                  onClick={() => {
                    setSelectedParentId(p.id);
                    if (p.children?.length) setSelectedChildId(p.children[0].id);
                  }}
                  className="w-full h-[40px] flex items-center text-left px-[4px] gap-[8px] rounded-[8px] hover:bg-[#EEF3F8] transition-colors"
                >
                  <img
                    src={
                      parentSelected
                        ? "/icons/folder-open-dot.svg"
                        : "/icons/folder-dot.svg"
                    }
                    alt=""
                    className="w-[18px] h-[18px] flex-shrink-0"
                  />
                  <span className="flex-1 text-[14px] font-medium leading-[14px] text-[#0B191F] truncate">
                    {p.name}
                  </span>
                </button>

                {/* CHILD ROWS */}
                {parentSelected && p.children?.length ? (
                  <div className="w-full flex flex-col gap-[4px] mt-[4px] mb-[8px]">
                    {p.children.map((c) => {
                      const childSelected = c.id === selectedChildId;

                      return (
                        <button
                          key={c.id}
                          type="button"
                          onClick={() => setSelectedChildId(c.id)}
                          className={`w-full h-[40px] flex items-center text-left pl-[20px] pr-[4px] gap-[4px] rounded-[8px] transition-colors
                            ${childSelected ? "bg-[#DCE3E5AD]" : "hover:bg-[#EEF3F8]"}
                          `}
                        >
                          <img
                            src="/icons/corner-down-right.svg"
                            alt=""
                            className="w-[14px] h-[14px] flex-shrink-0"
                          />
                          <span className="flex-1 text-[14px] font-medium leading-[14px] text-[#0B191F] truncate">
                            {c.name}
                          </span>
                        </button>
                      );
                    })}
                  </div>
                ) : null}
              </div>
            );
          })}
        </div>

        {filteredParents.length === 0 && (
          <p className="px-[4px] py-[12px] text-[13px] text-[#64748B]">
            No projects found.
          </p>
        )}
      </div>

      {/* USER PROFILE */}
       <div className="w-[212px] px-[12px] py-[12px] relative">

        <div className="w-full h-0 border-t border-[#DBE6EA] mb-[8px]" />
        <button
          type="button"
          onClick={() => setIsUserMenuOpen((prev) => !prev)}
          className="w-full h-[40px] flex items-center justify-between rounded-[8px] px-[8px] hover:bg-[#EEF3F8] transition-colors"
           >
          <div className="flex items-center gap-[8px] min-w-0 flex-1">
            <img
              src="/icons/Ellipse 1.svg"
              alt=""
              className="w-[24px] h-[24px] rounded-full flex-shrink-0"
            />
            <div className="min-w-0 text-left flex-1">
              <p className="text-[13px] font-medium text-[#0F172A] truncate">
                Amukelani Shringani
              </p>
              <p className="text-[12px] text-[#64748B] truncate">
                amushiringani@gmail.com
              </p>
            </div>
          </div>

          <img src="/icons/lucide.svg" alt="" className="w-[14px] h-[14px] flex-shrink-0 ml-[8px]" />
        </button>

        {isUserMenuOpen && (
          <div className="absolute left-[12px] bottom-[64px] w-[180px] bg-white border border-[#E5E7EB] rounded-lg shadow-md overflow-hidden">
            <button
              type="button"
              className="w-full text-left px-3 py-2 hover:bg-[#F8FAFC] text-[13px]"
            >
              Settings (placeholder)
            </button>
            <button
              type="button"
              className="w-full text-left px-3 py-2 hover:bg-[#F8FAFC] text-[13px]"
            >
              Logout (placeholder)
            </button>
          </div>
        )}
      </div>
    </aside>
  );
};

export default Sidebar;
