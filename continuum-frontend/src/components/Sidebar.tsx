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
    <aside className="w-[212px] h-screen bg-[#F7FBFF] border-r border-[#E9EEF5] flex flex-col">
      {/* TOP SECTION () */}
      <div className="w-[212px] flex flex-col gap-[16px]">
        {/* LOGO  */}
        <div className="w-[212px] h-[78px] pt-[32px] pb-[16px] flex items-start justify-center">
          <img
            src="/icons/Continuum (1).svg"
            alt="Continuum"
            className="w-[174px] h-[30px] object-contain"
          />
        </div>

        {/* SEARCH  */}
        <div className="w-[212px] h-[40px] rounded-full bg-[#EFF4FA] border border-[#E9EEF5] flex items-center gap-[8px] px-[12px]">
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
        <div className="w-[212px] h-[40px] flex gap-[8px]">
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
        <div className="w-[212px] h-[35px] flex items-center justify-between pt-[8px] pb-[8px]">
          <p className="w-[51px] h-[19px] text-[14px] font-medium leading-[14px] text-[#606D76]">
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

      {/* PROJECT LIST (scrollable) */}
      <div className="w-[212px] flex-1 overflow-y-auto pt-[4px]">
        {filteredParents.map((p) => {
          const parentSelected = p.id === selectedParentId;

          return (
            <div key={p.id} className="w-[212px]">
              {/* PARENT ROW */}
              <button
                type="button"
                onClick={() => {
                  setSelectedParentId(p.id);
                  if (p.children?.length) setSelectedChildId(p.children[0].id);
                }}
                className="w-[212px] h-[40px] flex items-center text-left pl-[12px] pr-[12px] gap-[8px] rounded-[8px]"
              >
                <img
                  src={
                    parentSelected
                      ? "/icons/folder-open-dot.svg"
                      : "/icons/folder-dot.svg"
                  }
                  alt=""
                  className="w-[18px] h-[18px]"
                />
                <span className="w-[164px] h-[19px] text-[14px] font-medium leading-[14px] text-[#0B191F] truncate">
                  {p.name}
                </span>
              </button>

              {/* CHILD ROWS (only when selected parent has children) */}
              {parentSelected && p.children?.length ? (
                <div className="w-[212px]">
                  {p.children.map((c) => {
                    const childSelected = c.id === selectedChildId;

                    return (
                      <button
                        key={c.id}
                        type="button"
                        onClick={() => setSelectedChildId(c.id)}
                        className={`w-[212px] h-[40px] flex items-center text-left pl-[24px] pr-[12px] gap-[4px] rounded-[8px]
                          ${childSelected ? "bg-[#DCE3E5AD]" : ""}
                        `}
                      >
                        <img
                          src="/icons/corner-down-right.svg"
                          alt=""
                          className="w-[14px] h-[14px]"
                        />
                        <span className="w-[164px] h-[19px] text-[14px] font-medium leading-[14px] text-[#0B191F] truncate">
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

        {filteredParents.length === 0 && (
          <p className="px-[12px] py-[12px] text-[13px] text-[#64748B]">
            No projects found.
          </p>
        )}
      </div>

      {/* USER PROFILE  */}
      <div className="w-[212px] border-t border-[#E9EEF5] p-[8px] relative">
        <button
          type="button"
          onClick={() => setIsUserMenuOpen((prev) => !prev)}
          className="w-[212px] h-[40px] flex items-center justify-between rounded-[8px] pr-[12px]"
        >
          <div className="flex items-center gap-[8px] min-w-0 pl-[12px]">
            <img
              src="/icons/Ellipse 1.svg"
              alt=""
              className="w-[24px] h-[24px] rounded-full"
            />
            <div className="min-w-0 text-left">
              <p className="text-[13px] font-medium text-[#0F172A] truncate">
                Amukelani Shringani
              </p>
              <p className="text-[12px] text-[#64748B] truncate">
                amushiringani@gmail.com
              </p>
            </div>
          </div>

          <img src="/icons/lucide.svg" alt="" className="w-[14px] h-[14px]" />
        </button>

        {isUserMenuOpen && (
          <div className="absolute left-[8px] bottom-[52px] w-[180px] bg-white border border-[#E5E7EB] rounded-lg shadow-md overflow-hidden">
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
