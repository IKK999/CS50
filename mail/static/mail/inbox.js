document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Send email
  document.querySelector('#compose-form').onsubmit = function(event) {
    event.preventDefault();
    send_email();
  }

  // By default, load the inbox
  load_mailbox('inbox');

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-content').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#form-header').innerHTML = "New Email";
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function compose_response(id) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-content').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Pre-fill composition fields
  document.querySelector('#form-header').innerHTML = "Reply";
  fetch(`emails/${id}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#compose-recipients').value = email.sender;
    document.querySelector('#compose-subject').value = (email.subject.slice(0, 4) === "Re: " ? email.subject : "Re: " + email.subject);
    document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: \n` + email.body + " => \n";
  });
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-content').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Output the messages
  output_emails(mailbox);
}

function open_email(is_sender, id) {

  // Show the opened email
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-content').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // output the details
  email_read(id);
  output_details(is_sender, id);
}

function send_email() {

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
    load_mailbox('sent');
    console.log("Email sent");
  });
}

function output_emails(mailbox) {
  fetch(`emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);

    for (let i = 0; i < emails.length; i++) {

      document.querySelector('#emails-view').innerHTML = document.querySelector('#emails-view').innerHTML + 
      `<a href="javascript:void(0);" onclick="open_email(${mailbox === 'sent'}, ${emails[i].id})">
      <div style="border: 1px solid black; margin: 3px; padding: 3px; color: black; background-color: ${emails[i].read ? "lightgray" : "white"};">
        <span><b>${mailbox === 'sent' ? emails[i].recipients : emails[i].sender}</b></span>
        <span style="margin-left: 5%;">${emails[i].subject}</span>
        <span style="float: right;">${emails[i].timestamp}</span>
      </div>
      </a>`;

    }
  });
}

function output_details(is_sender, id) {
  fetch(`emails/${id}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#email-content').innerHTML =
    `<p><b>From:</b> ${email.sender}</p>
      <p><b>To:</b> ${email.recipients}</p>
      <p><b>Subject:</b> ${email.subject}</p>
      <p><b>Timestamp:</b> ${email.timestamp}</p>
      <button class="btn btn-sm btn-outline-primary" onclick="compose_response(${id})">Reply</button>
      <hr>
      <p>${email.body}</p>
      ${is_sender ? `` : `<button class="btn btn-sm btn-outline-primary" onclick="email_archived(${id}, ${email.archived})">${email.archived ? "Unarchive" : "Archive"}</button>`}
      `;
  });

}

function email_read(id) {
  fetch(`emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
}

function email_archived(id, arch) {
  fetch(`emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !arch
    })
  })
  .then(() => {
    load_mailbox('inbox');
  });
}