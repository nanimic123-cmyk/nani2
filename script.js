
const careerData = {
  "Data Analyst": {
    skills: ["SQL", "Excel", "Python", "Power BI", "Statistics"],
    courses: [
      ["Google Data Analytics", "Google / Coursera", "Beginner", "Data analysis and visualization"],
      ["SQL for Data Analysis", "Learning platform", "Beginner", "SQL queries and databases"],
      ["Power BI Data Analyst", "Microsoft Learn", "Intermediate", "Dashboards and business intelligence"]
    ],
    certification: "Microsoft Power BI Data Analyst (PL-300)"
  },

  "Data Scientist": {
    skills: ["Python", "SQL", "Statistics", "Machine Learning", "Data Visualization"],
    courses: [
      ["Python for Data Science", "Learning platform", "Beginner", "Python and data handling"],
      ["Machine Learning Specialization", "DeepLearning.AI / Coursera", "Intermediate", "ML algorithms and models"],
      ["Statistics for Data Science", "Learning platform", "Intermediate", "Statistical foundations"]
    ],
    certification: "IBM Data Science Professional Certificate"
  },

  "Software Developer": {
    skills: ["Python", "Java", "Data Structures", "Problem Solving", "Git"],
    courses: [
      ["Programming Fundamentals", "Learning platform", "Beginner", "Programming concepts"],
      ["Data Structures and Algorithms", "Learning platform", "Intermediate", "Algorithmic problem solving"],
      ["Git and GitHub", "GitHub Skills", "Beginner", "Version control"]
    ],
    certification: "Oracle Java Certification"
  },

  "Web Developer": {
    skills: ["HTML", "CSS", "JavaScript", "React", "Git"],
    courses: [
      ["HTML and CSS Fundamentals", "Learning platform", "Beginner", "Website structure and styling"],
      ["JavaScript Essentials", "Learning platform", "Beginner", "Interactive web development"],
      ["React Development", "Learning platform", "Intermediate", "Modern frontend applications"]
    ],
    certification: "Meta Front-End Developer Certificate"
  },

  "Cybersecurity Analyst": {
    skills: ["Networking", "Linux", "Python", "Security Basics", "Risk Analysis"],
    courses: [
      ["Cybersecurity Fundamentals", "Cisco Networking Academy", "Beginner", "Security foundations"],
      ["Linux Essentials", "Learning platform", "Beginner", "Linux administration"],
      ["Network Security", "Learning platform", "Intermediate", "Network protection concepts"]
    ],
    certification: "CompTIA Security+"
  },

  "Cloud Engineer": {
    skills: ["Cloud Fundamentals", "Linux", "Networking", "Python", "Security Basics"],
    courses: [
      ["Cloud Fundamentals", "Microsoft Learn", "Beginner", "Cloud concepts"],
      ["AWS Cloud Practitioner Essentials", "AWS Skill Builder", "Beginner", "Cloud services"],
      ["Linux Administration", "Learning platform", "Intermediate", "Linux and server basics"]
    ],
    certification: "AWS Certified Cloud Practitioner"
  }
};

let student = JSON.parse(localStorage.getItem("careerStudent") || "null");
let completed = JSON.parse(localStorage.getItem("careerProgress") || "[]");

const $ = id => document.getElementById(id);

function normalize(value) {
  return value.trim().toLowerCase();
}

function showPage(page) {
  document.querySelectorAll(".page").forEach(section =>
    section.classList.toggle("active-page", section.id === page)
  );

  document.querySelectorAll(".nav").forEach(button =>
    button.classList.toggle("active", button.dataset.page === page)
  );
}

document.querySelectorAll(".nav").forEach(button => {
  button.addEventListener("click", () => showPage(button.dataset.page));
});

$("profileShortcut").addEventListener("click", () => showPage("profile"));

$("profileForm").addEventListener("submit", event => {
  event.preventDefault();

  student = {
    name: $("name").value.trim(),
    email: $("email").value.trim(),
    education: $("education").value,
    degree: $("degree").value.trim(),
    specialization: $("specialization").value.trim(),
    year: $("year").value,
    role: $("role").value,
    skills: $("skillsInput").value
      .split(",").map(normalize).filter(Boolean),
    softSkills: $("softSkills").value.trim()
  };

  localStorage.setItem("careerStudent", JSON.stringify(student));

  $("profileMessage").textContent =
    "Profile saved successfully. Your career analysis has been updated.";

  renderAll();
  showPage("careers");
});

function analyze() {
  if (!student) return null;

  const career = careerData[student.role];
  const matched = career.skills.filter(skill =>
    student.skills.includes(normalize(skill))
  );

  const missing = career.skills.filter(skill =>
    !student.skills.includes(normalize(skill))
  );

  const percentage = Math.round(
    matched.length / career.skills.length * 100
  );

  return { career, matched, missing, percentage };
}

function renderDashboard() {
  if (!student) return;

  const result = analyze();

  $("dashName").textContent = student.name;
  $("dashMatch").textContent = result.percentage + "%";
  $("dashSkills").textContent =
    result.matched.length + "/" + result.career.skills.length;

  const progress = result.missing.length
    ? Math.round(completed.length / result.missing.length * 100)
    : 100;

  $("dashProgress").textContent = Math.min(progress, 100) + "%";
}

function renderCareer() {
  if (!student) return;

  const result = analyze();

  $("careerResults").innerHTML = `
    <div class="result-card">
      <h2>${student.role}</h2>
      <p>Recommended career for ${escapeHTML(student.name)}</p>
      <div class="match-number">${result.percentage}%</div>
      <p>Current skill match</p>
      <div class="progress-track">
        <div class="progress-fill" style="width:${result.percentage}%"></div>
      </div>
      <p><b>Education:</b> ${escapeHTML(student.education)} - ${escapeHTML(student.degree)}</p>
      <p><b>Specialization:</b> ${escapeHTML(student.specialization)}</p>
      <p><b>Career Certification:</b> ${escapeHTML(result.career.certification)}</p>
    </div>
  `;
}

function renderSkills() {
  if (!student) return;

  const result = analyze();

  $("skillResults").innerHTML = `
    <div class="result-card">
      <h2>Skill Analysis: ${student.role}</h2>
      <p>Skill match: <b>${result.percentage}%</b></p>
      <div class="progress-track">
        <div class="progress-fill" style="width:${result.percentage}%"></div>
      </div>
      <h3>Existing Skills (${result.matched.length})</h3>
      <div class="skill-list">
        ${result.matched.map(skill =>
          `<span class="skill-tag">✓ ${skill}</span>`
        ).join("") || "No matching skills yet"}
      </div>
      <h3 style="margin-top:22px">Skills to Develop (${result.missing.length})</h3>
      <div class="skill-list">
        ${result.missing.map(skill =>
          `<span class="skill-tag skill-missing">+ ${skill}</span>`
        ).join("") || "You have all listed skills!"}
      </div>
    </div>
  `;
}

function renderCourses() {
  if (!student) return;

  const result = analyze();
  const relevantCourses = result.career.courses;

  $("courseResults").innerHTML = `
    <div class="result-card">
      <h2>Recommended for ${student.role}</h2>
      <p>These sample learning resources are selected to support your career goal.</p>
    </div>
    <div class="course-grid">
      ${relevantCourses.map((course, index) => `
        <div class="course-card">
          <h3>${course[0]}</h3>
          <p><b>Provider:</b> ${course[1]}</p>
          <p><b>Level:</b> ${course[2]}</p>
          <p>${course[3]}</p>
          <button class="primary add-course" data-index="${index}">
            Add to Learning Path
          </button>
        </div>
      `).join("")}
    </div>
    <div class="result-card" style="margin-top:18px">
      <h3>Suggested Professional Certification</h3>
      <p>${result.career.certification}</p>
    </div>
  `;

  document.querySelectorAll(".add-course").forEach(button => {
    button.addEventListener("click", () => {
      const task = "Course: " + relevantCourses[Number(button.dataset.index)][0];

      if (!completed.includes(task)) {
        completed.push(task);
        saveProgress();
        renderAll();
      }

      button.textContent = "Added ✓";
      button.disabled = true;
    });
  });
}

function renderPathway() {
  if (!student) return;

  const result = analyze();

  const tasks = [
    ...result.missing.map(skill => "Learn " + skill),
    "Course: " + result.career.courses[0][0],
    "Course: " + result.career.courses[1][0],
    "Course: " + result.career.courses[2][0],
    "Certification: " + result.career.certification
  ];

  const doneCount = tasks.filter(task => completed.includes(task)).length;
  const percentage = Math.round(doneCount / tasks.length * 100);

  $("pathwayResults").innerHTML = `
    <div class="result-card">
      <h2>Your ${student.role} Learning Plan</h2>
      <div class="match-number">${percentage}%</div>
      <p>Overall pathway completion</p>
      <div class="progress-track">
        <div class="progress-fill" style="width:${percentage}%"></div>
      </div>
      <p>${doneCount} of ${tasks.length} learning activities completed.</p>
    </div>
    <div class="result-card">
      <h2>Learning Activities</h2>
      ${tasks.map((task, index) => `
        <label class="path-item">
          <input type="checkbox"
            data-task="${encodeURIComponent(task)}"
            ${completed.includes(task) ? "checked" : ""}>
          <div>
            <h3>Step ${index + 1}: ${escapeHTML(task)}</h3>
            <p>${completed.includes(task) ? "Completed" : "Pending - mark when finished"}</p>
          </div>
        </label>
      `).join("")}
    </div>
  `;

  document.querySelectorAll("#pathwayResults input[type=checkbox]").forEach(box => {
    box.addEventListener("change", () => {
      const task = decodeURIComponent(box.dataset.task);

      if (box.checked && !completed.includes(task)) {
        completed.push(task);
      } else {
        completed = completed.filter(item => item !== task);
      }

      saveProgress();
      renderAll();
    });
  });
}

function saveProgress() {
  localStorage.setItem("careerProgress", JSON.stringify(completed));
}

function renderAll() {
  if (!student) return;

  renderDashboard();
  renderCareer();
  renderSkills();
  renderCourses();
  renderPathway();
}

function escapeHTML(value) {
  return String(value).replace(/[&<>"']/g, character => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
  })[character]);
}

// Load a realistic sample student to demonstrate the system
$("demoBtn").addEventListener("click", () => {
  student = {
    name: "Rahul Kumar",
    email: "rahul@example.com",
    education: "Undergraduate",
    degree: "B.Tech",
    specialization: "Computer Science",
    year: "2027",
    role: "Data Analyst",
    skills: ["python", "sql", "excel"],
    softSkills: "Communication, Teamwork"
  };

  completed = [];

  localStorage.setItem("careerStudent", JSON.stringify(student));
  saveProgress();

  $("name").value = student.name;
  $("email").value = student.email;
  $("education").value = student.education;
  $("degree").value = student.degree;
  $("specialization").value = student.specialization;
  $("year").value = student.year;
  $("role").value = student.role;
  $("skillsInput").value = "Python, SQL, Excel";
  $("softSkills").value = student.softSkills;

  renderAll();
  showPage("careers");
});

if (student) {
  $("name").value = student.name;
  $("email").value = student.email;
  $("education").value = student.education;
  $("degree").value = student.degree;
  $("specialization").value = student.specialization;
  $("year").value = student.year;
  $("role").value = student.role;
  $("skillsInput").value = student.skills.join(", ");
  $("softSkills").value = student.softSkills || "";
  renderAll();
}
