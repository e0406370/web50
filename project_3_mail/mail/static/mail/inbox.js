document.addEventListener('DOMContentLoaded', function() {

  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));

  document.querySelector('#compose-form').onsubmit = send_email;

  load_mailbox('inbox');
});

function compose_email() {

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

/**
 * @param {string} mailbox
 */
function load_mailbox(mailbox) {
  
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`, {
    method: "GET"
  })
    .then(resp => resp.json())
    .then(data => {
      if (data.length === 0) {
        const emptyMailbox = document.createElement('div');
        emptyMailbox.classList.add('alert', 'alert-info', 'text-center', 'font-weight-bold');
        emptyMailbox.innerHTML = 'This mailbox is empty. You are all caught up!';

        document.querySelector("#emails-view").append(emptyMailbox);
      }
      else {
        const emailContainer = document.createElement('div');
        emailContainer.classList.add('container');

        data.forEach(email => {
          const emailRow = document.createElement('div');
          emailRow.classList.add('row', 'border', 'border-light', 'font-weight-bold', 'mb-2', 'clickable_email_row');
          if (email.read) emailRow.classList.add('bg-secondary');

          const emailColSender = document.createElement('div');
          emailColSender.classList.add('col', 'text-left');
          emailColSender.innerHTML = email.sender;
          emailRow.appendChild(emailColSender);

          const emailColSubject = document.createElement('div');
          emailColSubject.classList.add('col');
          emailColSubject.innerHTML = email.subject;
          emailRow.appendChild(emailColSubject);

          const emailColTimestamp = document.createElement('div');
          emailColTimestamp.classList.add('col', 'text-right');
          emailColTimestamp.innerHTML = email.timestamp;
          emailRow.appendChild(emailColTimestamp);

          emailRow.addEventListener('click', () => {
            update_email(email.id, "read");
            load_email(email.id, mailbox);
          })

          emailContainer.appendChild(emailRow);
        });

        document.querySelector("#emails-view").append(emailContainer);
      }
    });
}

/**
 * @param {int} email_id
 * @param {string} mailbox
 */
function load_email(email_id, mailbox) {

  fetch(`/emails/${email_id}`, {
    method: "GET"
  })
    .then(resp => resp.json())
    .then(email => {
      const emailMetadata = document.createElement('table');
      emailMetadata.classList.add('table', 'border', 'text-white')
      emailMetadata.innerHTML = `
        <tbody>
          <tr>
            <th scope="row"> From </th>
            <td> ${email.sender} </td>
          </tr>
          <tr>
            <th scope="row"> To </th>
            <td> ${email.recipients} </td>
          </tr>
          <tr>
            <th scope="row"> Subject </th>
            <td> ${email.subject} </td>
          </tr>
          <tr>
            <th scope="row"> Timestamp </th>
            <td> ${email.timestamp} </td>
          </tr>
        </tbody>
      `

      const btnRow = document.createElement('div');
      btnRow.classList.add('row');

      const replyBtn = document.createElement('button');
      replyBtn.classList.add('btn', 'btn-primary', 'mb-2', 'ml-2');
      replyBtn.innerHTML = 'Reply';
      replyBtn.addEventListener('click', () => {
        reply_email(email);
      })
      btnRow.appendChild(replyBtn);

      const archiveBtn = document.createElement('button');
      const unarchiveBtn = document.createElement('button');

      if (mailbox === "inbox") {
        archiveBtn.classList.add('btn', 'btn-success', 'mb-2', 'ml-2');
        archiveBtn.innerHTML = 'Archive';
        archiveBtn.addEventListener('click', () => {
          update_email(email_id, "archive")
        })
        btnRow.appendChild(archiveBtn);
      }
      else if (mailbox === "archive") {
        unarchiveBtn.classList.add('btn', 'btn-danger', 'mb-2', 'ml-2');
        unarchiveBtn.innerHTML = 'Unarchive';
        unarchiveBtn.addEventListener('click', () => {
          update_email(email_id, "unarchive")
        })
        btnRow.appendChild(unarchiveBtn);
      }

      const emailBody = document.createElement('p');
      emailBody.classList.add('border', 'border-secondary', 'mb-2');
      emailBody.style.minHeight = '100px';
      emailBody.innerHTML = email.body;

      document.querySelector("#emails-view").innerHTML = '';
      document.querySelector("#emails-view").append(emailMetadata);
      document.querySelector("#emails-view").append(btnRow);
      document.querySelector("#emails-view").append(document.createElement('hr'));
      document.querySelector("#emails-view").append(emailBody);
    });
}

/**
 * @param {int} email_id
 * @param {string} param
 */
function update_email(email_id, param) {

  update_body = {}
  if (param === "read") update_body["read"] = true;
  if (param === "archive") update_body["archived"] = true;
  else if (param === "unarchive") update_body["archived"] = false;

  fetch(`/emails/${email_id}`, {
    method: "PUT",
    body: JSON.stringify(update_body),
  })
    .then(() => {
      if (param === "archive" || param === "unarchive") {
        load_mailbox('inbox');
      }
    });
}

/**
 * @param {any} original_email
 */
function reply_email(original_email) {

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  document.querySelector('#compose-recipients').value = original_email.sender;
  document.querySelector('#compose-subject').value = `${(!original_email.subject.trim().startsWith("Re:") ? 'Re:': '')}${original_email.subject}`;
  document.querySelector('#compose-body').value = `On ${original_email.timestamp} ${original_email.sender} wrote: \n${original_email.body}`;
}

/**
 * @param {SubmitEvent} event
 */
function send_email(event) {

  event.preventDefault();

  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: "POST",
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
    }),
  })
    .then(resp => resp.json().then(data => {
      if (!resp.ok) {
        alert(data.error);
      }
      else {
        alert(data.message);
        load_mailbox('sent');
      }
    }));
}