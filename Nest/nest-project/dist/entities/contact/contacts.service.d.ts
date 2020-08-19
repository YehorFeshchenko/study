import { Repository } from 'typeorm';
import Contact from './contact.entity';
import CreateContactDto from './../../dto/create-contact.dto';
export declare class ContactsService {
    private contactsRepository;
    constructor(contactsRepository: Repository<Contact>);
    getViewName(): string;
    findAll(): Promise<Contact[]>;
    findOne(id: string): Promise<Contact>;
    insert(contactDetails: CreateContactDto): Promise<Contact>;
    remove(id: string): Promise<void>;
}
