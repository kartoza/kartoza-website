-- Kartoza Hugo Site - Project-specific Neovim configuration
-- Provides whichkey shortcuts under <leader>p for project tasks

local ok, wk = pcall(require, "which-key")
if not ok then
  vim.notify("which-key not found, skipping project keybindings", vim.log.levels.WARN)
  return
end

-- Helper function to find unreviewed markdown files
local function find_unreviewed_pages()
  local content_dir = vim.fn.getcwd() .. "/content"
  local unreviewed = {}

  -- Use ripgrep to find all markdown files, then filter for those without reviewedBy
  local handle = io.popen('find "' .. content_dir .. '" -name "*.md" -type f 2>/dev/null')
  if not handle then
    return unreviewed
  end

  for file in handle:lines() do
    -- Skip _index.md files (section pages)
    if not file:match("_index%.md$") then
      local f = io.open(file, "r")
      if f then
        local content = f:read("*all")
        f:close()
        -- Check if file has front matter and reviewedBy field
        local front_matter = content:match("^%-%-%-(.-)%-%-%-")
        if front_matter then
          if not front_matter:match("reviewedBy:") then
            table.insert(unreviewed, file)
          end
        end
      end
    end
  end
  handle:close()

  return unreviewed
end

-- Show unreviewed pages in quickfix list
local function show_unreviewed_quickfix()
  local unreviewed = find_unreviewed_pages()
  if #unreviewed == 0 then
    vim.notify("All pages have been reviewed!", vim.log.levels.INFO)
    return
  end

  local qf_list = {}
  for _, file in ipairs(unreviewed) do
    table.insert(qf_list, {
      filename = file,
      lnum = 1,
      text = "Missing reviewedBy in front matter"
    })
  end

  vim.fn.setqflist(qf_list)
  vim.cmd("copen")
  vim.notify(string.format("Found %d unreviewed pages", #unreviewed), vim.log.levels.INFO)
end

-- Open next unreviewed page using Telescope
local function open_unreviewed_telescope()
  local has_telescope, telescope_builtin = pcall(require, "telescope.builtin")
  local unreviewed = find_unreviewed_pages()

  if #unreviewed == 0 then
    vim.notify("All pages have been reviewed!", vim.log.levels.INFO)
    return
  end

  if has_telescope then
    local pickers = require("telescope.pickers")
    local finders = require("telescope.finders")
    local conf = require("telescope.config").values
    local actions = require("telescope.actions")
    local action_state = require("telescope.actions.state")

    pickers.new({}, {
      prompt_title = "Unreviewed Pages (" .. #unreviewed .. " remaining)",
      finder = finders.new_table({
        results = unreviewed,
        entry_maker = function(entry)
          local display = entry:gsub(vim.fn.getcwd() .. "/content/", "")
          return {
            value = entry,
            display = display,
            ordinal = display,
          }
        end,
      }),
      sorter = conf.generic_sorter({}),
      attach_mappings = function(prompt_bufnr, map)
        actions.select_default:replace(function()
          actions.close(prompt_bufnr)
          local selection = action_state.get_selected_entry()
          vim.cmd("edit " .. selection.value)
        end)
        return true
      end,
    }):find()
  else
    -- Fallback to quickfix if telescope not available
    show_unreviewed_quickfix()
  end
end

-- Add reviewedBy to current file
local function add_reviewer_to_current()
  local reviewer = vim.fn.input("Reviewer name: ")
  if reviewer == "" then
    vim.notify("Cancelled - no reviewer name provided", vim.log.levels.WARN)
    return
  end

  local date = os.date("%Y-%m-%d")
  local bufnr = vim.api.nvim_get_current_buf()
  local lines = vim.api.nvim_buf_get_lines(bufnr, 0, -1, false)

  -- Find the end of front matter (second ---)
  local front_matter_end = nil
  local dash_count = 0
  for i, line in ipairs(lines) do
    if line:match("^%-%-%-") then
      dash_count = dash_count + 1
      if dash_count == 2 then
        front_matter_end = i
        break
      end
    end
  end

  if front_matter_end then
    -- Insert reviewedBy and reviewedDate before the closing ---
    local insert_line = front_matter_end - 1
    vim.api.nvim_buf_set_lines(bufnr, insert_line, insert_line, false, {
      'reviewedBy: "' .. reviewer .. '"',
      'reviewedDate: ' .. date,
    })
    vim.notify("Added reviewer: " .. reviewer, vim.log.levels.INFO)
  else
    vim.notify("Could not find front matter in this file", vim.log.levels.ERROR)
  end
end

-- Count unreviewed pages
local function count_unreviewed()
  local unreviewed = find_unreviewed_pages()
  vim.notify(string.format("Unreviewed pages: %d", #unreviewed), vim.log.levels.INFO)
end

-- Approve current file (auto-fill with git user name and today's date)
local function approve_current_file()
  -- Get git user name
  local handle = io.popen("git config user.name 2>/dev/null")
  local reviewer = ""
  if handle then
    reviewer = handle:read("*l") or ""
    handle:close()
  end

  if reviewer == "" then
    vim.notify("Could not get git user.name - please configure git", vim.log.levels.ERROR)
    return
  end

  local date = os.date("%Y-%m-%d")
  local bufnr = vim.api.nvim_get_current_buf()
  local lines = vim.api.nvim_buf_get_lines(bufnr, 0, -1, false)

  -- Check if file is a markdown file
  local filename = vim.api.nvim_buf_get_name(bufnr)
  if not filename:match("%.md$") then
    vim.notify("Not a markdown file", vim.log.levels.WARN)
    return
  end

  -- Check if already reviewed
  for _, line in ipairs(lines) do
    if line:match("^reviewedBy:") then
      vim.notify("File already has reviewedBy - use 'Add reviewer' to change", vim.log.levels.WARN)
      return
    end
  end

  -- Find the end of front matter (second ---)
  local front_matter_end = nil
  local dash_count = 0
  for i, line in ipairs(lines) do
    if line:match("^%-%-%-") then
      dash_count = dash_count + 1
      if dash_count == 2 then
        front_matter_end = i
        break
      end
    end
  end

  if front_matter_end then
    -- Insert reviewedBy and reviewedDate before the closing ---
    local insert_line = front_matter_end - 1
    vim.api.nvim_buf_set_lines(bufnr, insert_line, insert_line, false, {
      'reviewedBy: "' .. reviewer .. '"',
      'reviewedDate: ' .. date,
    })
    vim.notify("Approved by " .. reviewer .. " on " .. date, vim.log.levels.INFO)
  else
    vim.notify("Could not find front matter in this file", vim.log.levels.ERROR)
  end
end

-- Update reviewer to current git user and today's date (adds or updates)
local function update_reviewer()
  -- Get git user name
  local handle = io.popen("git config user.name 2>/dev/null")
  local reviewer = ""
  if handle then
    reviewer = handle:read("*l") or ""
    handle:close()
  end

  if reviewer == "" then
    vim.notify("Could not get git user.name - please configure git", vim.log.levels.ERROR)
    return
  end

  local date = os.date("%Y-%m-%d")
  local bufnr = vim.api.nvim_get_current_buf()
  local lines = vim.api.nvim_buf_get_lines(bufnr, 0, -1, false)

  -- Check if file is a markdown file
  local filename = vim.api.nvim_buf_get_name(bufnr)
  if not filename:match("%.md$") then
    vim.notify("Not a markdown file", vim.log.levels.WARN)
    return
  end

  -- Check if file is in content/ directory
  if not filename:match("/content/") then
    vim.notify("Not a content file", vim.log.levels.WARN)
    return
  end

  -- Find front matter boundaries and existing reviewer lines
  local front_matter_start = nil
  local front_matter_end = nil
  local reviewed_by_line = nil
  local reviewed_date_line = nil
  local dash_count = 0

  for i, line in ipairs(lines) do
    if line:match("^%-%-%-") then
      dash_count = dash_count + 1
      if dash_count == 1 then
        front_matter_start = i
      elseif dash_count == 2 then
        front_matter_end = i
        break
      end
    end
    if dash_count == 1 then
      if line:match("^reviewedBy:") then
        reviewed_by_line = i
      elseif line:match("^reviewedDate:") then
        reviewed_date_line = i
      end
    end
  end

  if not front_matter_end then
    vim.notify("Could not find front matter in this file", vim.log.levels.ERROR)
    return
  end

  -- Update or add reviewedBy
  if reviewed_by_line then
    lines[reviewed_by_line] = 'reviewedBy: "' .. reviewer .. '"'
  end

  -- Update or add reviewedDate
  if reviewed_date_line then
    lines[reviewed_date_line] = 'reviewedDate: ' .. date
  end

  -- If either is missing, add them before the closing ---
  if not reviewed_by_line or not reviewed_date_line then
    local insert_lines = {}
    if not reviewed_by_line then
      table.insert(insert_lines, 'reviewedBy: "' .. reviewer .. '"')
    end
    if not reviewed_date_line then
      table.insert(insert_lines, 'reviewedDate: ' .. date)
    end
    -- Insert before the closing ---
    for i, line in ipairs(insert_lines) do
      table.insert(lines, front_matter_end + i - 1, line)
    end
  end

  -- Write back all lines
  vim.api.nvim_buf_set_lines(bufnr, 0, -1, false, lines)
  vim.notify("Updated reviewer: " .. reviewer .. " on " .. date, vim.log.levels.INFO)
end

-- Hugo server commands
local function hugo_serve()
  vim.cmd("!hugo server -D &")
  vim.notify("Hugo server started", vim.log.levels.INFO)
end

local function hugo_build()
  vim.cmd("!hugo")
end

-- Script directory
local scripts_dir = vim.fn.getcwd() .. "/scripts"

-- Generic function to create new content and open the file
local function create_content(script_name, prompt_text)
  local title = vim.fn.input(prompt_text .. ": ")
  if title == "" then
    vim.notify("Cancelled", vim.log.levels.WARN)
    return
  end
  local cmd = string.format('%s/%s "%s"', scripts_dir, script_name, title)
  local handle = io.popen(cmd)
  if handle then
    local filepath = handle:read("*l")
    handle:close()
    if filepath and filepath ~= "" and not filepath:match("^Error") then
      vim.cmd("edit " .. filepath)
      vim.notify("Created: " .. filepath, vim.log.levels.INFO)
    else
      vim.notify("Failed to create content", vim.log.levels.ERROR)
    end
  end
end

-- Content creation functions
local function new_blog() create_content("new-blog.sh", "Blog title") end
local function new_app() create_content("new-app.sh", "App name") end
local function new_plugin() create_content("new-plugin.sh", "Plugin name") end
local function new_portfolio() create_content("new-portfolio.sh", "Project name") end
local function new_team() create_content("new-team-member.sh", "Team member name") end
local function new_training() create_content("new-training.sh", "Course title") end
local function new_docker() create_content("new-docker.sh", "Docker image name") end

-- Insert text at cursor position
local function insert_at_cursor(text)
  local lines = vim.split(text, "\n")
  local row, col = unpack(vim.api.nvim_win_get_cursor(0))
  vim.api.nvim_buf_set_text(0, row - 1, col, row - 1, col, lines)
  -- Move cursor to end of inserted text
  local new_row = row + #lines - 1
  local new_col = #lines > 1 and #lines[#lines] or col + #lines[1]
  vim.api.nvim_win_set_cursor(0, { new_row, new_col })
end

-- Shortcode insertion functions
local function insert_block()
  insert_at_cursor([[{{< block
    title="Title"
    subtitle="Subtitle"
    class="is-primary"
    sub-block-side="bottom"
>}}
Content here.
{{< /block >}}]])
end

local function insert_columns()
  insert_at_cursor([[{{< columns-start >}}
{{< column-start >}}

Column 1 content

{{< column-end >}}
{{< column-start >}}

Column 2 content

{{< column-end >}}
{{< columns-end >}}]])
end

local function insert_box()
  insert_at_cursor([[{{< box-start >}}

Box content here.

{{< box-end >}}]])
end

local function insert_rich_box()
  insert_at_cursor([[{{< rich-box-start >}}
{{< rich-content-start themeClass="is-primary" >}}

## Title

Content here.

{{< rich-content-end >}}
{{< rich-right-start >}}

![Image](/img/placeholder.png)

{{< rich-right-end >}}
{{< rich-box-end >}}]])
end

local function insert_image()
  insert_at_cursor([[{{< image
    src="/img/placeholder.png"
    alt="Description"
    caption="Caption text"
>}}]])
end

local function insert_button()
  insert_at_cursor([[{{< button
    link="https://example.com"
    text="Button Text"
    class="is-primary"
>}}]])
end

local function insert_button_bar()
  insert_at_cursor([[{{< button-bar >}}
{{< button link="https://example.com" text="Button 1" class="is-primary" >}}
{{< button link="https://example.com" text="Button 2" class="is-secondary" >}}
{{< /button-bar >}}]])
end

local function insert_tabs()
  insert_at_cursor([[{{< tabs >}}
{{< tab-content-start name="Tab 1" >}}

Tab 1 content

{{< tab-content-end >}}
{{< tab-content-start name="Tab 2" >}}

Tab 2 content

{{< tab-content-end >}}
{{< /tabs >}}]])
end

local function insert_spoiler()
  insert_at_cursor([[{{< spoiler-start title="Click to expand" >}}

Hidden content here.

{{< spoiler-end >}}]])
end

local function insert_info_bar()
  insert_at_cursor([[{{< info-bar
    title="Title"
    text="Information text here."
    class="is-info"
>}}]])
end

local function insert_feature()
  insert_at_cursor([[{{< feature
    title="Feature Title"
    description="Feature description."
    icon="fa-check"
>}}]])
end

local function insert_hero_banner()
  insert_at_cursor([[{{< hero-banner
    title="Hero Title"
    subtitle="Hero subtitle"
    background="/img/banner.png"
    class="is-primary"
>}}]])
end

-- Stats update functions
local function update_docker_stats()
  vim.cmd("!python3 " .. scripts_dir .. "/update-docker-stats.py")
end

local function update_plugin_stats()
  vim.cmd("!python3 " .. scripts_dir .. "/update-plugin-stats.py")
end

local function update_all_stats()
  vim.cmd("!python3 " .. scripts_dir .. "/update-all-stats.py")
end

local function update_docker_stats_dry()
  vim.cmd("!python3 " .. scripts_dir .. "/update-docker-stats.py --dry-run")
end

local function update_plugin_stats_dry()
  vim.cmd("!python3 " .. scripts_dir .. "/update-plugin-stats.py --dry-run")
end

-- ERPNext functions
local function fetch_erpnext_blogs()
  vim.cmd("!python3 " .. scripts_dir .. "/fetch-erpnext-blogs.py")
end

local function fetch_erpnext_blogs_dry()
  vim.cmd("!python3 " .. scripts_dir .. "/fetch-erpnext-blogs.py --dry-run")
end

local function fetch_erpnext_blogs_list()
  vim.cmd("!python3 " .. scripts_dir .. "/fetch-erpnext-blogs.py --list")
end

local function fetch_erpnext_portfolio()
  vim.cmd("!python3 " .. scripts_dir .. "/fetch-erpnext-portfolio.py")
end

local function fetch_erpnext_portfolio_list()
  vim.cmd("!python3 " .. scripts_dir .. "/fetch-erpnext-portfolio.py --list")
end

local function compare_erpnext_all()
  vim.cmd("!python3 " .. scripts_dir .. "/compare-erpnext-content.py")
end

local function compare_erpnext_verbose()
  vim.cmd("!python3 " .. scripts_dir .. "/compare-erpnext-content.py --verbose")
end

-- Linting and formatting functions
local function lint_current_file()
  local filename = vim.api.nvim_buf_get_name(0)
  if not filename:match("%.md$") then
    vim.notify("Not a markdown file", vim.log.levels.WARN)
    return
  end
  vim.cmd("!markdownlint --fix " .. vim.fn.shellescape(filename))
  vim.cmd("edit!")  -- Reload the file
  vim.notify("Markdown lint complete", vim.log.levels.INFO)
end

local function lint_all_content()
  vim.cmd("!markdownlint --fix 'content/**/*.md'")
  vim.notify("All content files linted", vim.log.levels.INFO)
end

local function format_current_file()
  local filename = vim.api.nvim_buf_get_name(0)
  if not filename:match("%.md$") then
    vim.notify("Not a markdown file", vim.log.levels.WARN)
    return
  end
  vim.cmd("!prettier --write --prose-wrap preserve " .. vim.fn.shellescape(filename))
  vim.cmd("edit!")  -- Reload the file
  vim.notify("Prettier formatting complete", vim.log.levels.INFO)
end

local function spell_check_current()
  local filename = vim.api.nvim_buf_get_name(0)
  if not filename:match("%.md$") then
    vim.notify("Not a markdown file", vim.log.levels.WARN)
    return
  end
  vim.cmd("!cspell --no-progress " .. vim.fn.shellescape(filename))
end

local function spell_check_content()
  vim.cmd("!cspell --no-progress 'content/**/*.md'")
end

local function add_word_to_dictionary()
  local word = vim.fn.expand("<cword>")
  if word == "" then
    word = vim.fn.input("Word to add: ")
  end
  if word == "" then
    vim.notify("No word provided", vim.log.levels.WARN)
    return
  end
  local dict_file = vim.fn.getcwd() .. "/.cspell/project-words.txt"
  local f = io.open(dict_file, "a")
  if f then
    f:write(word .. "\n")
    f:close()
    vim.notify("Added '" .. word .. "' to dictionary", vim.log.levels.INFO)
  else
    vim.notify("Could not open dictionary file", vim.log.levels.ERROR)
  end
end

local function run_all_checks()
  local filename = vim.api.nvim_buf_get_name(0)
  if not filename:match("%.md$") then
    vim.notify("Not a markdown file", vim.log.levels.WARN)
    return
  end
  vim.notify("Running all checks on current file...", vim.log.levels.INFO)
  vim.cmd("!markdownlint --fix " .. vim.fn.shellescape(filename) .. " && cspell --no-progress " .. vim.fn.shellescape(filename))
  vim.cmd("edit!")
end

-- Playwright test functions
local playwright_dir = vim.fn.getcwd() .. "/playwright/ci-test"

local function playwright_test_all()
  vim.cmd("!cd " .. playwright_dir .. " && npm test")
end

local function playwright_test_chromium()
  vim.cmd("!cd " .. playwright_dir .. " && npx playwright test --project=chromium")
end

local function playwright_test_firefox()
  vim.cmd("!cd " .. playwright_dir .. " && npx playwright test --project=firefox")
end

local function playwright_test_webkit()
  vim.cmd("!cd " .. playwright_dir .. " && npx playwright test --project=webkit")
end

local function playwright_test_headed()
  vim.cmd("!cd " .. playwright_dir .. " && npm run test:headed")
end

local function playwright_test_ui()
  vim.cmd("!cd " .. playwright_dir .. " && npm run test:ui &")
  vim.notify("Playwright UI started in background", vim.log.levels.INFO)
end

local function playwright_test_debug()
  vim.cmd("!cd " .. playwright_dir .. " && npm run test:debug")
end

local function playwright_show_report()
  vim.cmd("!cd " .. playwright_dir .. " && npm run report &")
  vim.notify("Playwright report opened in browser", vim.log.levels.INFO)
end

local function playwright_test_file()
  local filename = vim.api.nvim_buf_get_name(0)
  if not filename:match("%.spec%.ts$") then
    vim.notify("Not a Playwright spec file", vim.log.levels.WARN)
    return
  end
  local relative = filename:gsub(playwright_dir .. "/", "")
  vim.cmd("!cd " .. playwright_dir .. " && npx playwright test " .. vim.fn.shellescape(relative))
end

local function playwright_install()
  vim.cmd("!cd " .. playwright_dir .. " && npm install && npx playwright install")
  vim.notify("Playwright dependencies installed", vim.log.levels.INFO)
end

-- Register which-key mappings (flat structure for fewer key presses)
wk.add({
  { "<leader>p", group = "Project" },

  -- Hugo commands
  { "<leader>ps", hugo_serve, desc = "Serve" },
  { "<leader>pb", hugo_build, desc = "Build" },

  -- Review management
  { "<leader>pl", open_unreviewed_telescope, desc = "List unreviewed" },
  { "<leader>pq", show_unreviewed_quickfix, desc = "Quickfix unreviewed" },
  { "<leader>pr", update_reviewer, desc = "Update reviewer" },
  { "<leader>pa", approve_current_file, desc = "Approve (new only)" },
  { "<leader>pR", add_reviewer_to_current, desc = "Add reviewer (manual)" },
  { "<leader>p#", count_unreviewed, desc = "Count unreviewed" },

  -- New content (n = new)
  { "<leader>pn", group = "New content" },
  { "<leader>pnb", new_blog, desc = "Blog" },
  { "<leader>pna", new_app, desc = "App" },
  { "<leader>pnp", new_plugin, desc = "Plugin" },
  { "<leader>pnP", new_portfolio, desc = "Portfolio" },
  { "<leader>pnt", new_team, desc = "Team member" },
  { "<leader>pnT", new_training, desc = "Training" },
  { "<leader>pnd", new_docker, desc = "Docker" },

  -- Insert shortcodes (i = insert)
  { "<leader>pi", group = "Insert shortcode" },
  { "<leader>pib", insert_block, desc = "Block" },
  { "<leader>pic", insert_columns, desc = "Columns" },
  { "<leader>pix", insert_box, desc = "Box" },
  { "<leader>pir", insert_rich_box, desc = "Rich box" },
  { "<leader>pii", insert_image, desc = "Image" },
  { "<leader>piB", insert_button, desc = "Button" },
  { "<leader>piA", insert_button_bar, desc = "Button bar" },
  { "<leader>pit", insert_tabs, desc = "Tabs" },
  { "<leader>pis", insert_spoiler, desc = "Spoiler" },
  { "<leader>piI", insert_info_bar, desc = "Info bar" },
  { "<leader>pif", insert_feature, desc = "Feature" },
  { "<leader>pih", insert_hero_banner, desc = "Hero banner" },

  -- Update stats (u = update)
  { "<leader>pu", group = "Update stats" },
  { "<leader>pud", update_docker_stats, desc = "Docker stats" },
  { "<leader>pup", update_plugin_stats, desc = "Plugin stats" },
  { "<leader>pua", update_all_stats, desc = "All stats" },
  { "<leader>puD", update_docker_stats_dry, desc = "Docker (dry run)" },
  { "<leader>puP", update_plugin_stats_dry, desc = "Plugin (dry run)" },

  -- ERPNext (e = erpnext)
  { "<leader>pe", group = "ERPNext" },
  { "<leader>peb", fetch_erpnext_blogs, desc = "Sync blogs" },
  { "<leader>ped", fetch_erpnext_blogs_dry, desc = "Sync blogs (dry-run)" },
  { "<leader>peB", fetch_erpnext_blogs_list, desc = "List blogs" },
  { "<leader>pep", fetch_erpnext_portfolio, desc = "Fetch portfolio" },
  { "<leader>peP", fetch_erpnext_portfolio_list, desc = "List portfolio" },
  { "<leader>pec", compare_erpnext_all, desc = "Compare all" },
  { "<leader>peC", compare_erpnext_verbose, desc = "Compare verbose" },

  -- Linting and formatting (f = format/fix)
  { "<leader>pf", group = "Format/Lint" },
  { "<leader>pfl", lint_current_file, desc = "Lint file (markdownlint)" },
  { "<leader>pfL", lint_all_content, desc = "Lint all content" },
  { "<leader>pfp", format_current_file, desc = "Format file (prettier)" },
  { "<leader>pfs", spell_check_current, desc = "Spell check file" },
  { "<leader>pfS", spell_check_content, desc = "Spell check all" },
  { "<leader>pfa", run_all_checks, desc = "Run all checks" },
  { "<leader>pfw", add_word_to_dictionary, desc = "Add word to dictionary" },

  -- Playwright e2e tests (T = tests)
  { "<leader>pT", group = "Playwright tests" },
  { "<leader>pTa", playwright_test_all, desc = "Run all tests" },
  { "<leader>pTc", playwright_test_chromium, desc = "Chromium only" },
  { "<leader>pTf", playwright_test_firefox, desc = "Firefox only" },
  { "<leader>pTw", playwright_test_webkit, desc = "WebKit only" },
  { "<leader>pTh", playwright_test_headed, desc = "Headed mode" },
  { "<leader>pTu", playwright_test_ui, desc = "UI mode" },
  { "<leader>pTd", playwright_test_debug, desc = "Debug mode" },
  { "<leader>pTr", playwright_show_report, desc = "Show report" },
  { "<leader>pTt", playwright_test_file, desc = "Test current file" },
  { "<leader>pTi", playwright_install, desc = "Install deps" },

  -- Quick navigation
  { "<leader>pc", "<cmd>e content/<CR>", desc = "Content" },
  { "<leader>pL", "<cmd>e layouts/<CR>", desc = "Layouts" },
  { "<leader>pt", "<cmd>e themes/<CR>", desc = "Themes" },
  { "<leader>pS", "<cmd>e scripts/<CR>", desc = "Scripts" },
  { "<leader>pP", "<cmd>e playwright/ci-test/tests/<CR>", desc = "Playwright tests" },
})

vim.notify("Kartoza Hugo project config loaded. Use <leader>p for project commands.", vim.log.levels.INFO)
