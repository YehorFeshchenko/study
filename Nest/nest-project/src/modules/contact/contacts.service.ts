import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import Contact from './contact.entity';
import CreateContactDto from '../../dto/create-contact.dto';

@Injectable()
export class ContactsService {
  constructor(
    @InjectRepository(Contact)
    private contactsRepository: Repository<Contact>,
  ) { }

  findAll(): Promise<Contact[]> {
    return this.contactsRepository.find();
  }

  findOne(id: string): Promise<Contact> {
    return this.contactsRepository.findOne(id);
  }

  async insert(contactDetails: CreateContactDto): Promise<Contact> {
    const contact: Contact = Contact.create();
    const { firstName, lastName, phoneNumber, isActive } = contactDetails;
    contact.firstName = firstName;
    contact.lastName = lastName;
    contact.phoneNumber = phoneNumber;
    contact.isActive = isActive;
    await Contact.save(contact);
    return contact;
  }

  async remove(id: string): Promise<void> {
    await this.contactsRepository.delete(id);
  }
}