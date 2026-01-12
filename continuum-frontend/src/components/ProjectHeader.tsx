import { useState } from "react";

const ProjectHeader = () => {
  const [isClientVisible, setIsClientVisible] = useState(true);
  const [isExportOpen, setIsExportOpen] = useState(false);

  const projectName = "Untitled long project_name_1";
  const clientName = "Meta Technologies (Pty) Ltd";

  return (
    <div className="w-full">
      <div className="w-full h-[32px] flex items-center justify-between">

        <div className="h-[32px] flex items-center gap-[8px] min-w-0">
          <img
            src="/icons/folder-open-dot.svg"
            alt=""
            className="w-[16px] h-[16px] flex-shrink-0"
          />
          <p className="text-[13px] font-medium leading-[13px] text-[#0B191F] truncate">
            {projectName}
          </p>
        </div>

       
        <div className="h-[32px] flex items-center justify-end gap-[8px]">
          
          {isClientVisible && (
            <div
              className="w-[258px] h-[32px] rounded-full border border-[#E9EEF5] bg-[#EEF3F8]
                         px-[16px] py-[8px] flex items-center gap-[12px] min-w-0"
            >
              <img
                src="/icons/building-2.svg"
                alt=""
                className="w-[16px] h-[16px] flex-shrink-0"
              />

              <p className="text-[14px] font-medium leading-[14px] text-[#606D76] truncate">
                {clientName}
              </p>

              <button
                type="button"
                onClick={() => setIsClientVisible(false)}
                className="ml-auto w-[16px] h-[16px] flex items-center justify-center flex-shrink-0"
                title="Close client"
              >
                <img src="/icons/x.svg" alt="" className="w-[16px] h-[16px]" />
              </button>
            </div>
          )}

          {/* Bell */}
          <button
            type="button"
            className="w-[32px] h-[32px] rounded-[8px] bg-white border border-[#E9EEF5]
                       flex items-center justify-center"
            title="Notifications"
          >
            <img src="/icons/bell.svg" alt="" className="w-[16px] h-[16px]" />
          </button>

          {/* Share */}
          <button
            type="button"
            className="w-[93px] h-[32px] rounded-[8px] bg-white border border-[#E9EEF5]
                       px-[16px] py-[8px] flex items-center gap-[8px]"
            title="Share"
          >
            <img src="/icons/share.svg" alt="" className="w-[16px] h-[16px]" />
            <span className="text-[14px] font-medium leading-[14px] text-[#0B191F]">
              Share
            </span>
          </button>

          {/* Export dropdown */}
          <div className="relative">
            <button
              type="button"
              onClick={() => setIsExportOpen((prev) => !prev)}
              className="w-[94px] h-[32px] rounded-[8px]
                         px-[16px] pr-[12px] py-[8px]
                         flex items-center gap-[6px]
                         text-[14px] font-medium leading-[14px] text-white
                         bg-[linear-gradient(141.68deg,#24B5F8_-123.02%,#5521FE_802.55%)]"
            >
              Export
              <span className={`transition-transform ${isExportOpen ? "rotate-180" : ""}`}>
                {/* chevron-down icon */}
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  className="block"
                >
                  <path
                    d="M6 9L12 15L18 9"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </span>
            </button>

            {isExportOpen && (
              <div className="absolute right-0 top-[40px] w-[190px] bg-white border border-[#E5E7EB] rounded-[12px] shadow-md overflow-hidden z-50">
                <button
                  type="button"
                  onClick={() => setIsExportOpen(false)}
                  className="w-full text-left px-[12px] py-[10px] hover:bg-[#F8FAFC] text-[13px]"
                >
                  Export as PDF (placeholder)
                </button>
                <button
                  type="button"
                  onClick={() => setIsExportOpen(false)}
                  className="w-full text-left px-[12px] py-[10px] hover:bg-[#F8FAFC] text-[13px]"
                >
                  Export as CSV (placeholder)
                </button>
                <button
                  type="button"
                  onClick={() => setIsExportOpen(false)}
                  className="w-full text-left px-[12px] py-[10px] hover:bg-[#F8FAFC] text-[13px]"
                >
                  Export as PNG (placeholder)
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectHeader;
